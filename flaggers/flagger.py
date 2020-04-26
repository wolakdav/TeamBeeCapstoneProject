import abc
from enum import Enum, auto

class Flags(Enum):
  ###################################################
  # Documentation of flags can be found in flags.md
  ###################################################

  #Null flags
  ROW_ID_NULL = auto()
  SERVICE_DATE_NULL = auto()
  VEHICLE_NUMBER_NULL = auto()
  LEAVE_TIME_NULL = auto()
  TRAIN_NULL = auto()
  ROUTE_NUMBER_NULL = auto()
  DIRECTION_NULL = auto()
  SERVICE_KEY_NULL = auto()
  TRIP_NUMBER_NULL = auto()
  STOP_TIME_NULL = auto()
  ARRIVE_TIME_NULL = auto()
  DWELL_NULL = auto()
  LOCATION_ID_NULL = auto()
  DOOR_NULL = auto()
  ONS_NULL = auto()
  OFFS_NULL = auto()
  ESTIMATED_LOAD_NULL = auto()
  LIFT_NULL = auto()
  MAXIMUM_SPEED_NULL = auto()
  TRAIN_MILEAGE_NULL = auto()
  PATTERN_DISTANCE_NULL = auto()
  LOCATION_DISTANCE_NULL = auto()
  X_COORDINATE_NULL = auto()
  Y_COORDINATE_NULL = auto()
  DATA_SOURCE_NULL = auto()
  SCHEDULE_STATUS_NULL = auto()
  TRIP_ID_NULL = auto()

  #Unobserved stop flag
  UNOBSERVED_STOP = auto()

  #Unopened door flag
  UNOPENED_DOOR = auto()

  #Duplicate flag
  DUPLICATE = auto()

class Flagger(abc.ABC):
  # Name must be overwritten
  @property
  def name(self):
    raise NotImplementedError

  @abc.abstractmethod
  def flag(self, data):
    # Child classes must return a lit of flags.
    pass

flaggers = []
