import sys
import pandas
from src.tables.table import Table
from sqlalchemy.exc import SQLAlchemyError

class CTran_Data(Table):

    ###########################################################################
    # Public Methods

    def __init__(self, user=None, passwd=None, hostname="localhost", db_name="aperature", verbose=False, engine=None):
        super().__init__(user, passwd, hostname, db_name, verbose, engine)
        self._schema = "aperature"
        self._table_name = "ctran_data"
        self._index_col = "data_row"
        self._expected_cols = [
            "service_date",
            "vehicle_number",
            "leave_time",
            "train",
            "badge",
            "route_number",
            "direction",
            "service_key",
            "trip_number",
            "stop_time",
            "arrive_time",
            "dwell",
            "location_id",
            "door",
            "lift",
            "ons",
            "offs",
            "estimated_load",
            "maximum_speed",
            "train_mileage",
            "pattern_distance",
            "location_distance",
            "x_coordinate",
            "y_coordinate",
            "data_source",
            "schedule_status",
            "trip_id"
        ]

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

        # list(pandas.DataFrame) will get a list of the column names.
        if list(sample_data) != self._expected_cols:
            self._print("ERROR: the columns of read data does not match the specified columns.")
            return False

        if not self._create_table_helper(sample_data):
            return False

        self._print("Done.")
        return True

    ###########################################################################
    # Private Methods

    def _create_table_helper(self, sample_data):
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

        return True
