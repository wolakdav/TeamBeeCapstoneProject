from src.database import Database

###############################################################################
# Functions

def cli():
    aperature = Database()
    shouldExit = False
    options = [
        "(or ctrl-d) Exit.",
        "Print engine.",
        "Create ctran_data table.",
        "Delete ctran_data table.",
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

        shouldExit = _handle_switch_case(option, aperature)

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

def _handle_switch_case(option, database):
    if option == 0:
        print()
        return True

    elif option == 1:
        print(database.get_engine())

    elif option == 2:
        old_value = database.verbose
        database.verbose = True
        if not database.create_ctran_data():
            print("WARNING: an error occurred whlie building the ctran data.")
        database.verbose = old_value

    elif option == 3:
        if not database.delete_ctran_data():
            print("WARNING: an error occurred whlie deleting the ctran data.")

    else:
        raise RuntimeError("A case that should not be reached has been reached.")

    return False


###############################################################################
# Main

if __name__ == "__main__":
    # To skip entering username and password, supply them to this function.
    #my_engine = db_create.engine(hostname="db.cecs.pdx.edu", db="databees")
    cli()
