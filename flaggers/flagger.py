import abc
from enum import Enum

class Flags(Enum):
  ###################################################
  # Documentation of flags can be found in flags.txt.
  ###################################################

  #Null flags
  SERVICE_DATE_NULL = 1
  VEHICLE_NUMBER_NULL = 2
  LEAVE_TIME_NULL = 3
  TRAIN_NULL = 4
  BADGE_NULL = 5
  ROUTE_NUMBER_NULL = 6
  DIRECTION_NULL = 7
  SERVICE_KEY_NULL = 8
  TRIP_NUMBER_NULL = 9
  STOP_TIME_NULL = 10
  ARRIVE_TIME_NULL = 11
  DWELL_NULL = 12
  LOCATION_ID_NULL = 13
  DOOR_NULL = 14
  ONS_NULL = 15
  OFFS_NULL = 16
  ESTIMATED_LOAD_NULL = 17
  LIFT_NULL = 18
  MAXIMUM_SPEED_NULL = 19
  TRAIN_MILEAGE_NULL = 20
  PATTERN_DISTANCE_NULL = 21
  LOCATION_DISTANCE_NULL = 22
  X_COORDINATE_NULL = 23
  Y_COORDINATE_NULL = 24
  DATA_SOURCE_NULL = 25
  SCHEDULE_STATUS_NULL = 26
  TRIP_ID_NULL = 27


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
