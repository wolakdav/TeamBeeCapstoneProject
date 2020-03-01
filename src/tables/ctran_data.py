import sys
import pandas
from src.tables.table import Table
from sqlalchemy.exc import SQLAlchemyError

class CTran_Data(Table):

    ###########################################################################
    # Public Methods

    def __init__(self, user=None, passwd=None, hostname="localhost", db_name="aperature", verbose=False):
        super().__init__(user, passwd, hostname, db_name, verbose)
        self._schema = "aperature"
        self._index_col = "data_row"
        self._table_name = "ctran_data"
        self._creation_sql = "".join(["""
            CREATE TABLE IF NOT EXISTS """, self._schema, ".", self._table_name, """
            (
                data_row BIGSERIAL PRIMARY KEY,
                service_date DATE,
                vehicle_number INTEGER,
                leave_time INTEGER,
                train INTEGER,
                badge INTEGER,
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

    # NOTE: this method will likely fail if ran on a Windows machine.
    def create_table(self, ctran_sample_path="assets/"):
        csv_location = "".join([ctran_sample_path, "/ctran_trips_sample.csv"])
        self._print("Loading " + csv_location)
        sample_data = None
        try:
            sample_data = pandas.read_csv(csv_location, parse_dates=["service_date"])

        except FileNotFoundError as error:
            print("Pandas:", error)
            print("Cannot continue table creation, cancelling.")
            return False


        self._print("Connecting to DB.")
        try:
            with self._engine.connect() as conn:
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
        except ValueError as error:
            print("Pandas:", error)
            return False

        self._print("Done.")
        return True
