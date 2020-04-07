from flaggers.flagger import flaggers, Flags
import pytest


class DataRowNull():
  def __init__(self):
    self.row_id = None
    self.service_date = None
    self.vehicle_number = None
    self.leave_time = None
    self.train = None
    self.route_number = None
    self.direction = None
    self.service_key = None
    self.trip_number = None
    self.stop_time = None
    self.arrive_time = None
    self.dwell = None
    self.location_id = None
    self.door = None
    self.ons = None
    self.offs = None
    self.estimated_load = None
    self.lift = None
    self.maximum_speed = None
    self.train_mileage = None
    self.pattern_distance = None
    self.location_distance = None
    self.x_coordinate = None
    self.y_coordinate = None
    self.data_source = None
    self.schedule_status = None
    self.trip_id = None


class DataRowGood():
  def __init__(self):
    self.row_id = "good"
    self.service_date = "good"
    self.vehicle_number = "good"
    self.leave_time = "good"
    self.train = "good"
    self.route_number = "good"
    self.direction = "good"
    self.service_key = "good"
    self.trip_number = "good"
    self.stop_time = "good"
    self.arrive_time = "good"
    self.dwell = "good"
    self.location_id = "good"
    self.door = "good"
    self.ons = "good"
    self.offs = "good"
    self.estimated_load = "good"
    self.lift = "good"
    self.maximum_speed = "good"
    self.train_mileage = "good"
    self.pattern_distance = "good"
    self.location_distance = "good"
    self.x_coordinate = "good"
    self.y_coordinate = "good"
    self.data_source = "good"
    self.schedule_status = "good"
    self.trip_id = "good"


@pytest.fixture
def null_flagger():
  return [f for f in flaggers if f.name == 'Null'][0]

@pytest.fixture
def null_data_row():
  return vars(DataRowNull())

@pytest.fixture
def good_data_row():
  return vars(DataRowGood())


def test_null_flaggers_on_good_data(null_flagger, good_data_row):
  flags = null_flagger.flag(good_data_row)
  assert len(flags) == 0


def test_null_flaggers_on_null_data(null_flagger, null_data_row):
  flags = null_flagger.flag(null_data_row)
  assert len(flags) == len(null_data_row)
  assert Flags.ROW_ID_NULL in flags
  assert Flags.SERVICE_DATE_NULL in flags
  assert Flags.VEHICLE_NUMBER_NULL in flags
  assert Flags.LEAVE_TIME_NULL in flags
  assert Flags.TRAIN_NULL in flags
  assert Flags.ROUTE_NUMBER_NULL in flags
  assert Flags.DIRECTION_NULL in flags
  assert Flags.SERVICE_KEY_NULL in flags
  assert Flags.TRIP_NUMBER_NULL in flags
  assert Flags.STOP_TIME_NULL in flags
  assert Flags.ARRIVE_TIME_NULL in flags
  assert Flags.DWELL_NULL in flags
  assert Flags.LOCATION_ID_NULL in flags
  assert Flags.DOOR_NULL in flags
  assert Flags.ONS_NULL in flags
  assert Flags.OFFS_NULL in flags
  assert Flags.ESTIMATED_LOAD_NULL in flags
  assert Flags.LIFT_NULL in flags
  assert Flags.MAXIMUM_SPEED_NULL in flags
  assert Flags.TRAIN_MILEAGE_NULL in flags
  assert Flags.PATTERN_DISTANCE_NULL in flags
  assert Flags.LOCATION_DISTANCE_NULL in flags
  assert Flags.X_COORDINATE_NULL in flags
  assert Flags.Y_COORDINATE_NULL in flags
  assert Flags.DATA_SOURCE_NULL in flags
  assert Flags.SCHEDULE_STATUS_NULL in flags
  assert Flags.TRIP_ID_NULL in flags
