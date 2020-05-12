import getpass

class IOs:
    def __init__(self, verbose=False):
        self.verbose = verbose

    def prompt(self, prompt="", hide_input=False):
        return self._prompt(prompt, hide_input)

    def _prompt(self, prompt="", hide_input=False):
        while True:
            try:
                value = None
                if hide_input:
                    value = getpass.getpass(prompt)
                else:
                    value = input(prompt)
                return value
            except EOFError:
                print()

    def print(self, string, obj=None, force=False):
        return self._print(string, obj, force)

    def _print(self, string, obj=None, force=False):
        if not force:
            if not self.verbose:
                return

        if obj is None:
            print(string)

        else:
            print(string, end="")
            print(obj)