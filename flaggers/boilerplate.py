# Boiler plate code for flaggers.
# Do not change import line.
# Your class must implement the Flagger interface.
# To that end, your class must implement the flag method.
# Your flag method must return a list of flags. Flags are defined in flagger.py.
# You must append one instance of your class to flaggers.

from .flagger import Flagger, Flags, flaggers

class Boiler(Flagger):
  # Name is used for testing, but must be overwritten.
  name = 'Boilerplate'
  def flag(self, data):

    # ...

    # Must return a list of flags. Flags are defined in flagger.py
    return [Flags.INVALID, Flags.CONTAINS_NULL]
     
# Append an instance of your flagger to this list.
# Change Boiler to be your class.
flaggers.append(Boiler())
