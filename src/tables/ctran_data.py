import sys
import pandas
from .table import Table
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine.base import Engine

class CTran_Data(Table):

    ###########################################################################
    # Public Methods

    def __init__(self, user=None, passwd=None, hostname="localhost", db_name="aperture", verbose=False, engine=None):
        super().__init__(user, passwd, hostname, db_name, verbose, engine)
        self._schema = "aperture"
        self._table_name = "ctran_data"
        self._index_col = "row_id"
        self._expected_cols = set([
            "service_date",
            "vehicle_number",
            "leave_time",
            "train",
            "route_number",
            "direction",
            "service_key",
            "trip_number",
            "stop_time",
            "arrive_time",
            "dwell",
            "location_id",
            "door",
            "ons",
            "offs",
            "estimated_load",
            "lift",
            "maximum_speed",
            "train_mileage",
            "pattern_distance",
            "location_distance",
            "x_coordinate",
            "y_coordinate",
            "data_source",
            "schedule_status",
            "trip_id"
        ])

        self._creation_sql = "".join(["""
            CREATE TABLE IF NOT EXISTS """, self._schema, ".", self._table_name, """
            (
                row_id BIGSERIAL PRIMARY KEY,
                service_date DATE,
                vehicle_number INTEGER,
                leave_time INTEGER,
                train INTEGER,
                route_number INTEGER,
                direction SMALLINT,
                service_key CHARACTER(1),
                trip_number INTEGER,
                stop_time INTEGER,
                arrive_time INTEGER,
                dwell INTEGER,
                location_id INTEGER,
                door INTEGER,
                ons INTEGER,
                offs INTEGER,
                estimated_load INTEGER,
                lift INTEGER,
                maximum_speed INTEGER,
                train_mileage FLOAT,
                pattern_distance FLOAT,
                location_distance FLOAT,
                x_coordinate FLOAT,
                y_coordinate FLOAT,
                data_source INTEGER,
                schedule_status INTEGER,
                trip_id INTEGER
            );"""])

    #######################################################

    # [dev tool]
    # This will create a mock CTran Table for development purposes.
    def create_table(self, ctran_sample_path="assets/"):
        if not isinstance(self._engine, Engine):
            self._print("ERROR: self._engine is not an Engine, cannot continue.")
            return False

        csv_location = "".join([ctran_sample_path, "/ctran_trips_sample.csv"])
        self._print("Loading " + csv_location)

        sample_data = None
        try:
            sample_data = pandas.read_csv(csv_location, parse_dates=["service_date"])

        except (FileNotFoundError, ValueError) as error:
            print("Pandas:", error)
            print("Cannot continue table creation, cancelling.")
            return False

        if not self._check_cols(sample_data):
            self._print("ERROR: the columns of read data does not match the specified columns.")
            return False

        if not self._create_table_helper(sample_data):
            return False

        self._print("Done.")
        return True

    #######################################################

    # Query all data between date_from and date_to, dates
    # NOTE: if there is no ctran_data table, this will not work, obviously.
    # TODO confer with Sawyer over testing
    def query_date_range(self, date_from, date_to):
        if self._engine is None:
            self._print("ERROR: self._engine is None, cannot continue.")
            return None

        df = None
        sql = "".join(["SELECT * FROM ",
                       self._schema,
                       ".",
                       self._table_name,
                       " WHERE service_date BETWEEN '",
                       date_from.strftime("%Y-%m-%d"),
                       "' AND '",
                       date_to.strftime("%Y-%m-%d"),
                       "';"])
        self._print(sql)
        try:
            df = pandas.read_sql(sql, self._engine, index_col=self._index_col)

        except SQLAlchemyError as error:
            print("SQLAclchemy:", error)
            return None
        except (ValueError, KeyError) as error:
            print("Pandas:", error)
            return None

        if not self._check_cols(df):
            self._print("ERROR: the columns of read data does not match the specified columns.")
            return None

        return df

    ###########################################################################
    # Private Methods

    def _create_table_helper(self, sample_data):
        self._print("Connecting to DB.")
        try:
            conn = self._engine.connect()
            self._print("Initializing table.")
            if not super().create_table():
                self._print("ERROR: failed to create the table; cannot proceed.")
                return False

            self._print("Writing sample data to table. This will take a few minutes.")

            sample_data.to_sql(
                    self._table_name,
                    self._engine,
                    if_exists = "append",
                    index = False,
                    chunksize = self._chunksize,
                    schema = self._schema,
                )

        except SQLAlchemyError as error:
            print("SQLAclchemy:", error)
            return False
        except (KeyError, ValueError) as error:
            print("Pandas:", error)
            return False

        return True
