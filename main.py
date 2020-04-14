import os
import sys

from src.tables import CTran_Data
from src.tables import Flagged_Data
from src.tables import Flags
from src.tables import Service_Periods
from src.config import config
from src.interface import ArgInterface


##############################################################################
# Private Classes

class _Option():
    def __init__(self, msg, func_pointer):
        self.msg = msg
        self.func_pointer = func_pointer


###############################################################################
# Public Functions

def cli(read_env_data=False):
    def create_hive():
        flags.create_table()
        service_periods.create_table()
        flagged.create_table()

    ctran, flagged, flags, service_periods = _create_instances(read_env_data)

    if len(sys.argv) > 1:
        ai = ArgInterface()
        return ai.query_with_args(ctran, sys.argv[1:])


    options = [
        _Option("(or ctrl-d) Exit.", lambda: "Exit"),
        _Option("[dev tool] Create Aperature, the Portal mock DB [dev tool].", lambda: ctran.create_table()),
        _Option("Create Hive, the output point of the Data Pipeline.", lambda: create_hive()),
        _Option("Sub-menu: DB Operations", lambda: db_cli(ctran, flagged, flags, service_periods)),
    ]

    return _menu("Welcome to the CTran Data Marking Pipeline.", options)

###########################################################

def db_cli(ctran, flagged, flags, service_periods):
    def ctran_info():
        query = ctran.get_full_table()
        if query is None:
            print("WARNING: no data returned.")
        else:
            query.info()

    options = [
        _Option("(or ctrl-d) Exit.", lambda: "Exit"),
        _Option("Print engine.", lambda: print(ctran.get_engine())),
        _Option("[dev tool] Create aperture schema [dev tool].", ctran.create_schema),
        _Option("[dev tool] Delete aperture schema [dev tool].", ctran.delete_schema),
        _Option("[dev tool] Create mock ctran_data table [dev tool].", ctran.create_table),
        _Option("[dev tool] Delete mock ctran_data table [dev tool].", ctran.delete_table),
        _Option("Create hive schema.", flags.create_schema),
        _Option("Delete hive schema.", flags.delete_schema),
        _Option("Create flagged_data table.", flagged.create_table),
        _Option("Create flags table.", flags.create_table),
        _Option("Create service_periods table.", service_periods.create_table),
        _Option("Delete flagged_data table.", flagged.delete_table),
        _Option("Delete service_periods table.", flags.delete_table),
        _Option("Query ctran_data and print ctran_data.info().", ctran_info)
    ]

    return _menu("This is the Database Operations sub-menu.", options)

###############################################################################
# Private Functions

def _create_instances(read_env_data):
    config.load()
    try:
        if not read_env_data and os.environ["PIPELINE_ENV_DATA"]:
            read_env_data = True
    except KeyError as err:
        pass

    ctran = None
    if read_env_data:
        try:
            config.ingest_env()
            user = config.get_value('pipeline_user')
            passwd = config.get_value('pipeline_passwd')
            hostname = config.get_value('hostname')
            db_name = config.get_value('db_name')
            
        except KeyError as err:
            print("Could not read environment data " + str(err) + "; terminating.")
            return

        ctran = CTran_Data(user, passwd, hostname, db_name, verbose=True)
    else:
        ctran = CTran_Data(verbose=True)

    engine_url = ctran.get_engine().url
    flagged = Flagged_Data(verbose=True, engine=engine_url)
    flags = Flags(verbose=True, engine=engine_url)
    service_periods = Service_Periods(verbose=True, engine=engine_url)
    return ctran, flagged, flags, service_periods

###########################################################

# Option.func_pointer should return str "Exit" iff that option should cause the
# menu it is in to exit.
def _menu(title, options):
    if len(options) == 0:
        return

    msg = " ".join([str(title), "Please select what you would like to do:"])
    should_exit = False
    while not should_exit:
        print()
        print(msg)
        print()
        print()
        for i in range(len(options)):
            print(str(i) + ": " + options[i].msg)
        print()

        option = None
        try:
            option = _get_int(0, len(options)-1)
        except EOFError:
            option = 0

        if options[option].func_pointer() == "Exit":
            should_exit = True

###########################################################

def _get_int(min_value, max_value, cli_symbol="> "):
    should_continue = True
    while should_continue:
        try:
            option = input(cli_symbol)
            option = int(option)

            if option < min_value or option > max_value:
                print("{" + str(option) + "} is not within range [" + str(min_value) + ", " + str(max_value) + "]; try again.")
            else:
                should_continue = False

        except ValueError:
            print("Please enter an integer.")

    return option


###############################################################################
# Main

if __name__ == "__main__":
    cli()
