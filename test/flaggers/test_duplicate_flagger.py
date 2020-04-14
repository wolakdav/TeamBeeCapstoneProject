from flaggers.flagger import flaggers, Flags
import pytest

class DataRow():
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
def duplicate_flagger():
  return [f for f in flaggers if f.name == 'Duplicate'][0]

#Create list with just 1 item
@pytest.fixture
def good_data():
	full_list = []
	full_list.append(vars(DataRow()))
	return full_list

#Create list with 2 same items
@pytest.fixture
def bad_data():
	full_list = []
	full_list.append(vars(DataRow()))
	full_list.append(vars(DataRow()))
	return full_list

#Should NOT return a flags, since data is good [returns empty list]
def test_duplicate_flagger_on_good_data(duplicate_flagger, good_data):
	flags = duplicate_flagger.flag(good_data[0], good_data)
	assert len(flags) == 0

#Should return flags, since data is bad [returns list with 1 flag]
def test_duplicate_flagger_on_bad_data(duplicate_flagger, bad_data):
	flags = duplicate_flagger.flag(bad_data[0], bad_data)
	assert len(flags) == 1