# TODO: build unit tests; see Nelson's test suite branch when pushed.
from src.tables.ctran_data import CTran_Data
from src.tables.duplicated_data import Duplicated_Data

###############################################################################
# Functions

def cli():
    # TODO: Current, both of these prompt for user/passwd; only have one do it.
    #   Possibly have the constructor take an engine and just leave user/passwd
    #   blank. If engine is supplied, (possibly) extract user/passwd/hostname/db_name
    portal = CTran_Data()
    duplicates = Duplicated_Data()

    shouldExit = False
    # TODO: have another list that maps each option index to a function pointer
    #   better yet, have each value of a list be a struct w/ message and function values
    options = [
        "(or ctrl-d) Exit.",             # 0
        "Print engine.",                 # 1
        "",
        "Create aperature schema.",      # 2
        "Delete aperature schema.",      # 3
        "",
        "Create ctran_data table.",      # 4
        "Create duplicates table.",      # 5
        "",
        "Delete ctran_data table.",      # 6
        "Delete duplicates table.",      # 7
        "",
        "Query ctran_data and print ctran_data.info().", # 8
    ]

    while not shouldExit:
        print()
        print("This is the StopSpot data pipeline. Please select what you would like to do:")
        print()
        print()
        offset = 0
        for i in range(len(options)):
            value = options[i]
            if value == "":
                print()
                offset += 1
            else:
                print(str(i-offset) + ": " + value)
        print()

        option = None
        try:
            option = _get_int(0, len(options)-1)
        except EOFError:
            option = 0

        shouldExit = _handle_switch_case(option, portal, duplicates)

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

def _handle_switch_case(option, ctran, duplicates):
    if option == 0:
        print()
        return True

    elif option == 1:
        ctran.print_engine()

    elif option == 2:
        ctran.create_schema()

    elif option == 3:
        ctran.delete_schema()

    elif option == 4:
        old_value = ctran.verbose
        ctran.verbose = True
        if not ctran.create_table():
            print("WARNING: an error occurred whlie building the ctran_data.")
        ctran.verbose = old_value

    elif option == 5:
        old_value = duplicates.verbose
        duplicates.verbose = True
        if not duplicates.create_table():
            print("WARNING: an error occurred whlie building the duplicates.")
        duplicates.verbose = old_value

    elif option == 6:
        if not ctran.delete_table():
            print("WARNING: an error occurred whlie deleting the ctran data.")

    elif option == 7:
        if not ctran.delete_table():
            print("WARNING: an error occurred whlie deleting the duplicates.")

    elif option == 8:
        query = ctran.get_full_table()
        query.info()

    else:
        raise RuntimeError("A case that should not be reached has been reached.")

    return False


###############################################################################
# Main

if __name__ == "__main__":
    cli()
