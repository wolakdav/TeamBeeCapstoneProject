import abc
from enum import Enum

class Flags(Enum):
  # Documentation of flags can be found in flags.txt.
  INVALID = 1
  CONTAINS_NULL = 2

  #Null flags
  SERVICE_DATE_NULL = 3
  VEHICLE_NUMBER_NULL = 4
  LEAVE_TIME_NULL = 5
  TRAIN_NULL = 6
  BADGE_NULL = 7
  ROUTE_NUMBER_NULL = 8
  DIRECTION_NULL = 9
  SERVICE_KEY_NULL = 10
  TRIP_NUMBER_NULL = 11
  STOP_TIME_NULL = 12
  ARRIVE_TIME_NULL = 13
  DWELL_NULL = 14
  LOCATION_ID_NULL = 15
  DOOR_NULL = 16
  ONS_NULL = 17
  OFFS_NULL = 18
  ESTIMATED_LOAD_NULL = 19
  LIFT_NULL = 20
  MAXIMUM_SPEED_NULL = 21
  TRAIN_MILEAGE_NULL = 22
  PATTERN_DISTANCE_NULL = 23
  LOCATION_DISTANCE_NULL = 24
  X_COORDINATE_NULL = 25
  Y_COORDINATE_NULL = 26
  DATA_SOURCE_NULL = 27
  SCHEDULE_STATUS_NULL = 28
  TRIP_ID_NULL = 29

class Flagger(abc.ABC):
  @abc.abstractmethod
  def flag(self, data):
    # Child classes must return a lit of flags.
    pass

flaggers = []
