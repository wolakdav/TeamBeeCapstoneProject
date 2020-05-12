import abc
from enum import IntEnum, auto

class Flags(IntEnum):
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

flag_descriptions = {
  Flags.ROW_ID_NULL : "ROW_ID_NULL",
  Flags.SERVICE_DATE_NULL : "SERVICE_DATE_NULL",
  Flags.VEHICLE_NUMBER_NULL : "VEHICLE_NUMBER_NULL",
  Flags.LEAVE_TIME_NULL : "LEAVE_TIME_NULL",
  Flags.TRAIN_NULL : "TRAIN_NULL",
  Flags.ROUTE_NUMBER_NULL : "ROUTE_NUMBER_NULL",
  Flags.DIRECTION_NULL : "DIRECTION_NULL",
  Flags.SERVICE_KEY_NULL : "SERVICE_KEY_NULL",
  Flags.TRIP_NUMBER_NULL : "TRIP_NUMBER_NULL",
  Flags.STOP_TIME_NULL : "STOP_TIME_NULL",
  Flags.ARRIVE_TIME_NULL : "ARRIVE_TIME_NULL",
  Flags.DWELL_NULL : "DWELL_NULL",
  Flags.LOCATION_ID_NULL : "LOCATION_ID_NULL",
  Flags.DOOR_NULL : "DOOR_NULL",
  Flags.ONS_NULL : "ONS_NULL",
  Flags.OFFS_NULL : "OFFS_NULL",
  Flags.ESTIMATED_LOAD_NULL : "ESTIMATED_LOAD_NULL",
  Flags.LIFT_NULL : "LIFT_NULL",
  Flags.MAXIMUM_SPEED_NULL : "MAXIMUM_SPEED_NULL",
  Flags.TRAIN_MILEAGE_NULL : "TRAIN_MILEAGE_NULL",
  Flags.PATTERN_DISTANCE_NULL : "PATTERN_DISTANCE_NULL",
  Flags.LOCATION_DISTANCE_NULL : "LOCATION_DISTANCE_NULL",
  Flags.X_COORDINATE_NULL : "X_COORDINATE_NULL",
  Flags.Y_COORDINATE_NULL : "Y_COORDINATE_NULL",
  Flags.DATA_SOURCE_NULL : "DATA_SOURCE_NULL",
  Flags.SCHEDULE_STATUS_NULL : "SCHEDULE_STATUS_NULL",
  Flags.TRIP_ID_NULL : "TRIP_ID_NULL",
  Flags.UNOBSERVED_STOP : "UNOBSERVED_STOP",
  Flags.UNOPENED_DOOR : "UNOPENED_DOOR",
  Flags.DUPLICATE : "DUPLICATE",
}

flaggers = []
