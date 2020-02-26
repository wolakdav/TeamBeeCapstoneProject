
###############################################################################
# Public Functions

def cli():
    shouldExit = False
    options = [
            "(or ctrl-d) Exit."
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

        shouldExit = _handle_switch_case(option)


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

###########################################################

def _handle_switch_case(option):
    if option == 0:
        print()
        return True

    else:
        raise RuntimeError("A case that should not be reached has been reached.")

    return False


###############################################################################
# Main

if __name__ == "__main__":
    cli()
