import pandas

from .table import Table
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine.base import Engine

class Service_Periods(Table):

    def __init__(self, user=None, passwd=None, hostname=None, db_name=None, schema="hive", verbose=False, engine=None):
        super().__init__(user, passwd, hostname, db_name, schema, verbose, engine)
        self._table_name = "service_periods"
        self._index_col = "service_key"
        self._expected_cols = [
            "start_date",
            "end_date",
        ]
        self._creation_sql = "".join(["""
            CREATE TABLE IF NOT EXISTS """, self._schema, ".", self._table_name, """
            (
                service_key BIGSERIAL PRIMARY KEY,
                start_date DATE NOT NULL,
                end_date DATE NOT NULL,
                UNIQUE (start_date, end_date)
            );"""])

    
    def write_table(self, dates):
        # Dates: list of datetime dates. Only important value in the dates are
        # month and year.
        # NOTE: not currently being used but could be useful in the future.
        data = []
        for date in dates:
            data.append([date.month, date.year, self.get_ternary(date.month)])
        df = pandas.DataFrame(data, columns=self._expected_cols)
        # service_key is BIGSERIAL so there should never be a conflict.
        return self._write_table(df)  


    def query(self, date):
        # Find a service_periods row that matches the month and year.
        # Note that ternary isn't included because that's derived from month.

        if not isinstance(self._engine, Engine):
            self._print("ERROR: invalid engine.")
            return None
        service_key = None

        sql = "".join(["SELECT * FROM ", self._schema, ".", self._table_name,
                       " WHERE ", date.strftime("'%Y-%m-%d'"),
                       " BETWEEN start_date AND end_date;"
                       ])
        try:
            with self._engine.connect() as con:
                result = con.execute(sql)
                if result.rowcount != 0:
                    return result.first()['service_key']
        except SQLAlchemyError as error:
            print("SQLAlchemy: ", error)
            return None


    def insert_one(self, date):
        # Insert a row and return the id.
        # Honestly should be using write_table() but the RETURNING
        # functionality isn't built into write_table() and I'm too lazy to
        # add that functionality right now so I'll save it for a TODO.
        if not isinstance(self._engine, Engine):
            self._print("ERROR: invalid engine.")
            return None

        start_date, end_date = self.get_service_period(date)
        sql = "".join(["INSERT INTO ", self._schema, ".", self._table_name,
                       " (start_date, end_date) VALUES (",
                       start_date.strftime("'%Y-%m-%d'"), ', ',
                       end_date.strftime("'%Y-%m-%d'"),
                       ") RETURNING service_key;"])
        try:
            with self._engine.connect() as con:
                result = con.execute(sql)
                return result.first()[0]
        except SQLAlchemyError as error:
            print("SQLAlchemy: ", error)
            return None


    def query_or_insert(self, date):
        # Retrieves the service_key of a matched service_periods.
        # If none exist, insert a new one and return its service_key.
        period = self.query(date)
        if period:
            return period 
        
        return self.insert_one(date)
        

    def get_service_period(self, date):
        # Convert date to service periods in the format of (start_date, end_date)
        # These values are not confirmed by user and may change in the future.
        # Placeholder separators for service periods:
        # Jan 10, May 10, Sep 10
        separator = [datetime(date.year-1, 9, 10),
                     datetime(date.year,   1, 10),
                     datetime(date.year,   5, 10),
                     datetime(date.year,   9, 10),
                     datetime(date.year+1, 1, 10)]

        for i in range(len(separator)):
            if date >= separator[i] and date < separator [i+1]:
                return (separator[i], separator[i+1] - timedelta(days=1))

        return None  # Should never happen.
