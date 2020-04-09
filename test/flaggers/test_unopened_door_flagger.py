from flaggers.flagger import flaggers, Flags
import pytest

#Data is good when door opens at least once during the stop
class GoodData():
	def __init__(self):
		self.door = 1

#Data is bad when door does NOT open during the stop
class BadData():
	def __init__(self):
		self.door = 0

@pytest.fixture
def unopened_door_flagger():
  return [f for f in flaggers if f.name == 'UnopenedDoor'][0]

@pytest.fixture
def good_data:
	return vars(GoodData())

@pytest.fixture
def bad_data:
	return vars(BadData())

#Should NOT return a flags, since data is good [returns empty list]
def test_unopened_door_flagger_on_good_data(unopened_door_flagger, good_data):
	flags = unopened_door_flagger.flag(good_data)
	assert len(flags) == 0

#Should return flags, since data is bad [returns list with 1 flag]
def test_unopened_door_flagger_on_bad_data(unopened_door_flagger, bad_data):
	flags = unopened_door_flagger.flag(bad_data)
	assert len(flags) == 1