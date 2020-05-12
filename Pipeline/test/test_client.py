import pytest
from src.client import _Client

@pytest.fixture
def mock_config():
    class Mock_Config:
        def __init__(self):
            self._data = {}

        def load(self, read_env_data=False):
            self._data = {
                "portal_user": "aperture",
                "portal_passwd": "dummy",
                "portal_hostname": "LaLaLand",
                "portal_db_name": "portal",
                "pipeline_user": "pipeline",
                "pipeline_passwd": "fake",
                "pipeline_hostname": "localhost",
                "pipeline_db_name": "hive"
            }
            return True

        def get_value(self, value):
            if value in self._data:
                return self._data[value]

    return Mock_Config()

@pytest.fixture
def instance_fixture(mock_config):
    client_instance = _Client(read_env_data=False)
    client_instance.config = mock_config
    return client_instance


def test_instance_fixture(instance_fixture):
    instance_fixture
    assert True

def test_create_hive(instance_fixture):
    class Custom_Table():
        def __init__(self):
            self.value = 0

        def create_table(self):
            self.value += 1

    custom = Custom_Table()

    instance_fixture.flags = custom
    instance_fixture.service_periods = custom
    instance_fixture.flagged = custom
    instance_fixture.create_hive()
    assert custom.value == 3
