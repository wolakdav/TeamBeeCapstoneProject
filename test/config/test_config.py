import pytest
import os
import json
from datetime import datetime
from src.config import config
from src.config import BoundsResult


@pytest.fixture
def empty_config():
    return config

@pytest.fixture
def loaded_config(tmp_path):
    mock_config = {
        "email": "test@test.com",
        "pipeline_user": "sw23",
        "pipeline_passwd": "fake",
        "pipeline_hostname": "localhost",
        "pipeline_db_name": "aperature",
        "columns": { "vehicle_number": { "max": "NA", "min": 0 }, "maximum_speed" : {"max" : 150, "min" : 0}, "service_date" : {"max" : "NA", "min" : "1990-01-01"} }
    }

    p = tmp_path / "test_config.json"
    p.write_text(json.dumps(mock_config))
    config.load(p)
    return config
    
def test_get_set_config(empty_config):
    config.set_value("test", 5)
    assert config.get_value("test") == 5

def test_ingest_env(monkeypatch, empty_config):
    monkeypatch.setenv("PIPELINE_USER", "test_user")
    monkeypatch.setenv("PIPELINE_PASSWD", "test_pass")
    empty_config.ingest_env()

    assert empty_config.get_value("pipeline_user") == "test_user"
    assert empty_config.get_value("pipeline_passwd") == "test_pass"

def test_load_config(tmp_path):
    mock_config = {
        "email": "test@test.com",
        "pipeline_user": "sw23",
        "pipeline_passwd": "fake",
        "pipeline_hostname": "localhost",
        "pipeline_db_name": "aperature",
        "columns": { "vehicle_number": { "max": "NA", "min": 0 } }
    }

    p = tmp_path / "test_config.json"
    p.write_text(json.dumps(mock_config))
    
    assert p.read_text() == json.dumps(mock_config)
    
    config_dict = json.loads(p.read_text())
    assert config_dict["email"] == mock_config["email"]

def test_check_bounds(loaded_config):
    assert loaded_config.check_bounds("vehicle_number", 2) == BoundsResult.VALID
    
    assert loaded_config.check_bounds("maximum_speed", 180) == BoundsResult.MAX_ERROR
    assert loaded_config.check_bounds("maximum_speed", -1) == BoundsResult.MIN_ERROR

    good_date_str = '2011-01-03'
    bad_date_str = '1970-01-03'

    assert loaded_config.check_bounds("service_date", good_date_str) == BoundsResult.VALID
    assert loaded_config.check_bounds("service_date", bad_date_str) == BoundsResult.MIN_ERROR


