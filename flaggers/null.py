from .flagger import Flagger, Flags, flaggers

class Null(Flagger):
  def flag(self, data):
    # DUDE YOUR DATA HAS A NULL IN IT!!!!
    return [Flags.CONTAINS_NULL]
     
flaggers.append(Null())
