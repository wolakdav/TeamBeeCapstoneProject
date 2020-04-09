from flaggers.flagger import flaggers, Flags
import pytest

class GoodData():
	def __init__(self):
		self.location_distance = 0

class BadData():
	def __init__(self):
		#location_distance should be set from .env, but currently check unopenedDoor.py for value: 50
		self.location_distance = 666

@pytest.fixture
def unobserved_stop_flagger():
  return [f for f in flaggers if f.name == 'UnobservedStop'][0]

@pytest.fixture
def good_data:
	return vars(GoodData())

@pytest.fixture
def bad_data:
	return vars(BadData())

#Should NOT return a flags, since data is good [returns empty list]
def test_unobserved_stop_flagger_on_good_data(unobserved_stop_flagger, good_data):
	flags = unobserved_stop_flagger.flag(good_data)
	assert len(flags) == 0

#Should return flags, since data is bad [returns list with 1 flag]
def test_unobserved_stop_flagger_on_bad_data(unobserved_stop_flagger, bad_data):
	flags = unobserved_stop_flagger.flag(bad_data)
	assert len(flags) == 1

