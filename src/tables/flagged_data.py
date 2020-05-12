import datetime
from sqlalchemy.engine.base import Engine
from sqlalchemy.exc import SQLAlchemyError
import pandas

from .table import Table
import flaggers.flagger as flagger


class Flagged_Data(Table):

    def __init__(self, user=None, passwd=None, hostname=None, db_name=None, schema="hive", verbose=False, engine=None):
        super().__init__(user, passwd, hostname, db_name, schema, verbose, engine)
        self._table_name = "flagged_data"
        self._index_col = None
        self._expected_cols = [
            "row_id",
            "service_key",
            "flag_id",
            "service_date"
        ]
        # flag_id is ON UPDATE CASCADE to anticipate flags table changing.
        # service_key shouldn't change.
        self._creation_sql = "".join(["""
            CREATE TABLE IF NOT EXISTS """, self._schema, ".", self._table_name, """
            (
                row_id INTEGER,
                service_key INTEGER REFERENCES """, self._schema, """.service_periods(service_key),
                flag_id INTEGER REFERENCES """, self._schema, """.flags(flag_id) ON UPDATE CASCADE,
                service_date DATE NOT NULL,
                PRIMARY KEY (flag_id, service_key, row_id)
            );"""])

    #######################################################

    def write_table(self, data):
        # data is list of [row_id, flag_id, service_key].
        if data == []:
            self._print("ERROR: write_table recieved no data to write, cancelling.")
            return False
        df = pandas.DataFrame(data, columns=[
            "row_id",
            "service_key",
            "flag_id",
            "service_date"
            ])
        return self._write_table(df, 
                 conflict_columns=["row_id", "flag_id", "service_key"])

    #######################################################

# SELECT *
# FROM
#      aperture.flagged_data AS fd,
#      aperture.service_periods AS sp
# WHERE
#       fd.row_id = '10'
# AND
#       sp.year = '2019'
# AND
#       sp.ternary = '1'
# AND
#       fd.service_key = sp.service_key;
    def query_by_row_id(self, sp_table, row_id, service_year, service_period):
        sql = "".join(["SELECT * FROM ",
                       self._schema,
                       ".",
                       self._table_name,
                       " AS fd, ",
                       self._schema,
                       ".",
                       sp_table,
                       " AS sp, WHERE fd.row_id = '",
                       row_id,
                       "' AND sp.year = '",
                       service_year,
                       "' AND sp.ternary = '",
                       service_period,
                       "' AND fd.service_key = sp.service_key"
                       ";"])

        return self._query_table(sql)

    #######################################################

    def query_by_flag_id(self, flag_id, limit):
        sql = "".join(["SELECT * FROM ",
                       self._schema,
                       ".",
                       self._table_name,
                       " WHERE flag_id = '",
                       flag_id,
                       "' LIMIT '",
                       limit,
                       "';"])

        return self._query_table(sql)

    #######################################################

    # Return the latest day (as datetime) stored, None if no days are stored.
    def get_latest_day(self):
        value = None
        sql = "".join(["SELECT MAX(service_date) ",
                       "FROM ", self._schema, ".", self._table_name,
                       ";"])
        self._print(sql)
        self._print("Connecting to DB.")
        conn = self._engine.connect()
        value = conn.execute(sql)
       
        if value is not None:
            self._print("Done")
            return value.first()[0]
        else:
            return None

    #######################################################

    # start_date and end_date can be string dates in YYYY/MM/DD, datetimes, or
    # None. If end_date is none, the start_date will be used for that value. If
    # dates are backwards, they will be flipped.
    def delete_date_range(self, start_date, end_date=None):
        if not isinstance(self._engine, Engine):
            self._print("ERROR: invalid engine.")
            return False

        start_date, end_date = self._process_dates(start_date, end_date)
        if start_date is None:
            self._print("ERROR: could not determine the date(s).")
            return False

        values_sql = []
        dates = self._get_date_range(start_date, end_date)
        if dates is None:
            self._print("ERROR: could not determine the date(s).")
            return False

        for date in dates:
            values_sql.append(
                "".join(["'", str(date.year), "/", str(date.month), "/", str(date.day), "'"])
            )
        values_sql = ", ".join(values_sql)
        sql = "".join(["DELETE FROM ", self._schema, ".", self._table_name,
                       " WHERE service_date IN (", values_sql, ");"])
        self._print(sql)

        self._print("Connecting to DB.")
        conn = self._engine.connect()
        conn.execute(sql)


        self._print("Done")
        return True

    #######################################################

    # Get a list of date value(s) b/w day and end_date.
    # day and end_date can be strings in YYYY/MM/DD or datetime instances.
    def _get_date_range(self, day, end_date=None):
        dates = []
        try:
            if not isinstance(day, datetime.date):
                dates.append(datetime.datetime.strptime(day, "%Y/%m/%d"))
            else:
                dates.append(day)
            if end_date is not None:
                if not isinstance(end_date, datetime.date):
                    end_date = datetime.datetime.strptime(end_date, "%Y/%m/%d")
                delta = datetime.timedelta(days=1)
                curr_date = dates[0]
                curr_date += delta
                while curr_date < end_date:
                    dates.append(curr_date)
                    curr_date += delta
                dates.append(end_date)
        except ValueError:
            self._print("ERROR: The input date is malformed; please use the YYYY/MM/DD format.")
            return None

        return dates

    #######################################################

    # start_date and end_date can be string dates in YYYY/MM/DD, datetimes, or
    # None. If end_date is none, the start_date will be used for that value. If
    # dates are backwards, they will be flipped.
    # On success, this returns: start_date, end_date as datetimes; on failure,
    # this returns None, None.
    def _process_dates(self, start_date, end_date=None):
        def _convert_to_date(string, criteria):
            try:
                if isinstance(string, str):
                    string = datetime.datetime.strptime(string, "%Y/%m/%d")
                elif not isinstance(string, datetime.datetime) or not isinstance(string, datetime.date):
                    raise ValueError
            except ValueError:
                return None
            return string

        start_date = _convert_to_date(start_date, "start")
        if start_date is None:
            return None, None

        if end_date is None:
            end_date = start_date
        else:
            end_date = _convert_to_date(end_date, "end  ")

        if start_date < end_date:
            return start_date, end_date
        else:
            return end_date, start_date


    def create_view_for_flag(self, flag):
        # flag is one of flagger's Flags enum.
        view_name = "view_" + flagger.flag_descriptions[flag]
        sql = "".join([
            "CREATE VIEW ", self._schema, ".", view_name, " AS\n",
            "SELECT * FROM ", self._schema, ".", self._table_name,
            " WHERE flag_id=", str(flag.value), ";"
        ])

        with self._engine.connect() as con:
            con.execute(sql)

        self._print("Done")
        return True


    def create_views_all_flags(self):
        # Create a view for all available flag, return false if any failed.
        status = True
        for flag in flagger.Flags:
            if not self.create_view_for_flag(flag):
                status = False
        return status
