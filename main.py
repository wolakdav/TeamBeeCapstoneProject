# TODO: build unit tests; see Nelson's test suite branch when pushed.
#   When getting started, give everything one last assumption check.
from src.tables.ctran_data import CTran_Data
from src.tables.duplicated_data import Duplicated_Data
from src.tables.flagged_data import Flagged_Data
from src.tables.flags import Flags


##############################################################################
# Private Classes

class _Option():
    # func_pointer should return str "Exit" iff that option should cause main to
    # exit.
    def __init__(self, msg, func_pointer):
        self.msg = msg
        self.func_pointer = func_pointer


###############################################################################
# Public Functions

def cli():
    ctran = CTran_Data(verbose=True)
    engine_url = ctran.get_engine().url
    duplicates = Duplicated_Data(verbose=True, engine=engine_url)
    flagged = Flagged_Data(verbose=True, engine=engine_url)
    flags = Flags(verbose=True, engine=engine_url)

    def ctran_info():
        query = ctran.get_full_table()
        if query is None:
            print("WARNING: no data returned.")
        else:
            query.info()

    should_exit = False
    options = [
        _Option("(or ctrl-d) Exit.", lambda: "Exit"),
        _Option("Print engine.", lambda: print(ctran.get_engine())),
        _Option("Create aperature schema.", ctran.create_schema),
        _Option("Delete aperature schema.", ctran.delete_schema),
        _Option("Create ctran_data table.", ctran.create_table),
        _Option("Create duplicates table.", duplicates.create_table),
        _Option("Create flagged_data table.", flagged.create_table),
        _Option("Create flags table.", flags.create_table),
        _Option("Delete ctran_data table.", ctran.delete_table),
        _Option("Delete duplicates table.", duplicates.delete_table),
        _Option("Delete flagged_data table.", flagged.delete_table),
        _Option("Delete flags table.", flags.delete_table),
        _Option("Query ctran_data and print ctran_data.info().", ctran_info)
    ]

    while not should_exit:
        print()
        print("This is the StopSpot data pipeline. Please select what you would like to do:")
        print()
        print()
        for i in range(len(options)):
            value = options[i]
            print(str(i) + ": " + options[i].msg)
        print()

        option = None
        try:
            option = _get_int(0, len(options)-1)
        except EOFError:
            option = 0

        if options[option].func_pointer() == "Exit":
            should_exit = True


###############################################################################
# Private Functions

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
