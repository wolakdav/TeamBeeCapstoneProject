
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
    should_exit = False
    options = [
        _Option("(or ctrl-d) Exit.", lambda: "Exit"),
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
