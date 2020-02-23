import getpass
import pandas
from sqlalchemy import create_engine

###############################################################################
# "Public" Functions

# To skip entering username and password, supply them to this function.
def engine(user=None, passwd=None, hostname="localhost", db="aperature", verbose=False):
    if user is None:
        user = _get_name()

    if passwd is None:
        passwd = _get_passwd()

    engine_info = ["postgresql://", user, ":", passwd, "@", hostname, "/", db]
    engine = create_engine("".join(engine_info))

    if verbose:
        print("Your engine has been created: ", end = "")
        print(engine)

    return engine

###########################################################

# TODO: see what happens if this runs on windows since '/'
#   could also check which OS it is and use the correct slash
# TODO: send this a faulty engine, and one without permissions
# TODO: see what exceptions can be thrown by conn
def ctran_data(engine, ctran_sample_path="models/assets/", verbose=True):
    if verbose:
        print("Loading ctran_trips_sample.csv")

    sample_df = pandas.read_csv(ctran_sample_path + "ctran_trips_sample.csv", parse_dates=["service_date"])

    with engine.connect() as conn:
        if verbose:
            print("Initializing table.")

        if not _create_ctran_table(conn):
            if verbose:
                print("Failed to create the table; exiting.")
            return False

    if verbose:
        print("Writing sample data to table.")
        print("\tThis will take a minute or two.")

    sample_df.to_sql(
            "ctran_data",
            engine,
            if_exists = "append",
            index = False,
            chunksize = 500,
            schema = "public",
            )

    if verbose:
        print("Done.")
    return True


###############################################################################
# "Private" functions

# TODO: catch that invalid SQL exception and return false
def _create_ctran_table(conn):
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

###########################################################

def _get_name():
    while True:
        try:
            user = input("Enter username: ")
            return user
        except EOFError:
            print()

###########################################################

def _get_passwd():
    while True:
        try:
            passwd = getpass.getpass("Enter password: ")
            return passwd
        except EOFError:
            print()

