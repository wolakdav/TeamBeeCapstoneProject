# TODO: build unit tests; see Nelson's test suite branch when pushed.
from src.tables.ctran_data import CTran_Data
from src.tables.duplicated_data import Duplicated_Data


##############################################################################
# Private Classes

class _Option():
    # funcPointer should return str "Exit" iff that option should cause main to
    # exit.
    def __init__(self, msg, funcPointer):
        self.msg = msg
        self.funcPointer = funcPointer


###############################################################################
# Public Functions

def cli():
    # TODO: Current, both of these prompt for user/passwd; only have one do it.
    #   Possibly have the constructor take an engine and just leave user/passwd
    #   blank. If engine is supplied to constructor, extract
    #   user/passwd/hostname/db_name
    ctran = CTran_Data()
    duplicates = Duplicated_Data()
    ctran.verbose = True
    duplicates.verbose = True

    def ctran_info():
        query = ctran.get_full_table()
        query.info()

    shouldExit = False
    options = [
        _Option("(or ctrl-d) Exit.", lambda: "Exit"),
        _Option("Print engine.", ctran.print_engine),
        _Option("Create aperature schema.", ctran.create_schema),
        _Option("Delete aperature schema.", ctran.delete_schema),
        _Option("Create ctran_data table.", ctran.create_table),
        _Option("Create duplicates table.", duplicates.create_table),
        _Option("Delete ctran_data table.", ctran.delete_table),
        _Option("Delete duplicates table.", duplicates.delete_table),
        _Option("Query ctran_data and print ctran_data.info().", ctran_info)
    ]

    while not shouldExit:
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

        if options[option].funcPointer() == "Exit":
            shouldExit = True


###############################################################################
# Private Functions

def _get_int(min_value, max_value, cli_symbol="> "):
    shouldContinue = True
    while shouldContinue:
        try:
            option = input(cli_symbol)
            option = int(option)

            if option < min_value or option > max_value:
                print("{" + str(option) + "} is not within range [" + str(min_value) + ", " + str(max_value) + "]; try again.")
            else:
                shouldContinue = False

        except ValueError:
            print("Please enter an integer.")

    return option


###############################################################################
# Main

if __name__ == "__main__":
    cli()
