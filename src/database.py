import getpass
import pandas
from sqlalchemy import create_engine

# This class will contain all of the methods to address the db.
class Database():
    # TODO: create/get other tables

    ###########################################################################
    # Public Methods

    def __init__(self, user=None, passwd=None, hostname="localhost", db_name="aperature", verbose=False):
        self.user = user
        if user is None:
            self.user = self._prompt("Enter username: ")

        self.passwd = passwd
        if passwd is None:
            self.passwd = self._prompt("Enter password: ", hide=True)

        self.hostname = hostname
        self.db_name = db_name
        self.verbose = verbose
        self.rebuild_engine()

    #######################################################

    def rebuild_engine(self):
        engine_info = ["postgresql://", self.user, ":", self.passwd, "@", self.hostname, "/", self.db_name]
        self._engine = create_engine("".join(engine_info))

        if self.verbose:
            print("Your engine has been created: ", end = "")
            print(self._engine)
        
        return True

    #######################################################

    def get_engine(self):
        return self._engine

    #######################################################
    
    def get_ctran_data(self):
        return pandas.read_sql("SELECT * FROM ctran_data;", self._engine, index_col="data_row")

    #######################################################
    
    # TODO: see what happens if this runs on windows since '/'
    #   could also check which OS it is and use the correct slash
    # TODO: send this a faulty engine, and one without permissions
    # TODO: see what exceptions can be thrown by conn
    # exception: psycopg2.errors.AdminShutdown
    # exception: sqlalchemy.exc.OperationalError
    def create_ctran_data(self, ctran_sample_path="assets/"):
        if self.verbose:
            print("Loading ctran_trips_sample.csv")

        # TODO: catch the error based on not finding the path
        temp_df = pandas.read_csv(ctran_sample_path + "/ctran_trips_sample.csv", parse_dates=["service_date"])

        with self._engine.connect() as conn:
            if self.verbose:
                print("Initializing table.")

            if not self._create_ctran_table(conn):
                if self.verbose:
                    print("Failed to create the table; exiting.")
                return False

        if self.verbose:
            print("Writing sample data to table.")
            print("\tThis will take a minute or three, unless the DB is not local; then this will take like five minutes.")

        temp_df.to_sql(
                "ctran_data",
                self._engine,
                if_exists = "append",
                index = False,
                chunksize = 500,
                schema = "public",
                )

        if self.verbose:
            print("Done.")
        return True

    #######################################################

    # TODO: catch that invalid SQL exception and return false
    # or if the table already exists - sqlalchemy.exc.ProgrammingError
    def delete_ctran_data(self):
        with self._engine.connect() as conn:
            conn.execute("""
                    DROP TABLE "ctran_data";
                    """)
        return True

    ###########################################################################
    # Private Methods

    def _prompt(self, prompt="", hide=False):
        while True:
            try:
                value = None
                if hide:
                    value = getpass.getpass(prompt)
                else:
                    value = input(prompt)
                return value
            except EOFError:
                print()

    #######################################################

    # TODO: catch that invalid SQL exception and return false
    def _create_ctran_table(self, conn):
        conn.execute("""
                CREATE TABLE IF NOT EXISTS ctran_data
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
                );
                """)

        return True

