import models.create
import models.delete


###############################################################################
# Functions

def cli(engine):
    shouldExit = False

    while not shouldExit:
        print()
        print("This is the StopSpot data pipeline. Please select what you would like to do:")
        print()
        print("0 (or ctrl-d): Exit.")
        print("1: Print engine.")
        print("2: Create ctran_data table.")
        print("3: Delete ctran_data table.")
        print()

        option = None
        try:
            option = _get_int(0, 3)
        except EOFError:
            option = 0

        shouldExit = _handle_switch_case(option, engine)

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

def _handle_switch_case(option, engine):
    if option == 0:
        print()
        return True

    elif option == 1:
        print(engine)

    elif option == 2:
        if not models.create.ctran_data(engine):
            print("WARNING: an error occurred whlie building the ctran data.")

    elif option == 3:
        if not models.delete.ctran_data(engine):
            print("WARNING: an error occurred whlie deleting the ctran data.")

    else:
        raise RuntimeError("A case that should not be reached has been reached.")

    return False


###############################################################################
# Main

if __name__ == "__main__":
    # To skip entering username and password, supply them to this function.
    my_engine = models.create.engine(hostname="db.cecs.pdx.edu", db="databees")
    cli(my_engine)

