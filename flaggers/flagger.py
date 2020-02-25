import abc
from enum import Enum

class Flags(Enum):
  # Documentation of flags can be found in [TODO].
  INVALID = 1
  CONTAINS_NULL = 2

class Flagger(abc.ABC):
  @abc.abstractmethod
  def flag(self, data):
    # Child classes must return a lit of flags.
    pass

flaggers = []
