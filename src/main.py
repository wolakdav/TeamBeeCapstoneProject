# TODO: put table.py and ctran_data.py in src/databases/
# TODO: put table.py and ctran_data.py into src w/ init file
# TODO: build unit tests; see Nelson's test suite branch when pushed.
from tables.ctran_data import CTran_Data

###############################################################################
# Functions

def cli():
    portal = CTran_Data()
    shouldExit = False
    options = [
        "(or ctrl-d) Exit.",
        "Print engine.",
        "Create portal schema.",
        "Delete portal schema.",
        "Create ctran_data table.",
        "Delete ctran_data table.",
        "Query ctran_data and print ctran_data.info().",
    ]

    while not shouldExit:
        print()
        print("This is the StopSpot data pipeline. Please select what you would like to do:")
        print()
        for i in range(len(options)):
            print(str(i) + ": " + options[i])
        print()

        option = None
        try:
            option = _get_int(0, len(options)-1)
        except EOFError:
            option = 0

        shouldExit = _handle_switch_case(option, portal)

###########################################################

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

###########################################################

def _handle_switch_case(option, portal):
    if option == 0:
        print()
        return True

    elif option == 1:
        portal.print_engine()

    elif option == 2:
        portal.create_schema()

    elif option == 3:
        portal.delete_schema()

    elif option == 4:
        old_value = portal.verbose
        portal.verbose = True
        if not portal.create_table():
            print("WARNING: an error occurred whlie building the ctran data.")
        portal.verbose = old_value

    elif option == 5:
        if not portal.delete_table():
            print("WARNING: an error occurred whlie deleting the ctran data.")

    elif option == 6:
        query = portal.get_full_table()
        query.info()

    else:
        raise RuntimeError("A case that should not be reached has been reached.")

    return False


###############################################################################
# Main

if __name__ == "__main__":
    # To skip entering username and password, supply them to this function.
    #my_engine = db_create.engine(hostname="db.cecs.pdx.edu", db="databees")
    cli()
