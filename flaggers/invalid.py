from .flagger import Flagger, Flags, flaggers

class Invalid(Flagger):
  def flag(self, data):
    # YOUR DATA IS PURE GARBAGE.
    return [Flags.INVALID]
     
#flaggers.append(Invalid())
