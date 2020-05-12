from src.notif import _Notif
import pytest
import io

@pytest.fixture
def mock_config():
    class Mock_Config:
        def __init__(self):
            self._data = {
            	"notif_django_path": "output/notif.txt"
            }

        def get_value(self, value):
            if value in self._data:
                return self._data[value]

    return Mock_Config()

@pytest.fixture
def instance(mock_config):
    return _Notif(mock_config)

#Django returns true on successful write to a file
def test_django_write_success(instance):
	result = instance.django('Test message')
	assert result == True

#Returns False when can't write to a file: in this case use specified non-existend folder aka wrong path
def test_django_write_fail(monkeypatch, instance):
	instance._config._data.pop("notif_django_path")
	monkeypatch.setattr("sys.stdin", io.StringIO("non_existent_folder/test_notif.txt" + "\n"))
	result = instance.django('Test message')
	assert result == False

#Tests ability to specify path if path is absent from assets/config.json
def test_django_user_defined_valid_path(monkeypatch, instance):
	instance._config._data.pop("notif_django_path")
	monkeypatch.setattr("sys.stdin", io.StringIO("output/test_notif.txt" + "\n"))
	result = instance.django('Test message')
	assert result == True

#Tests ability to specify wrong path, in which case write will fail
def test_django_user_defined_invalid_path(monkeypatch, instance):	
	instance._config._data.pop("notif_django_path")
	monkeypatch.setattr("sys.stdin", io.StringIO("non_existent_folder/test_notif.txt" + "\n"))
	result = instance.django('Test message')
	assert result == False