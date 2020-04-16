import pytest
import os
import json
from datetime import datetime
from src.config import config
from src.config import BoundsResult


MOCK_CONFIG = {
        "email": "test@test.com",
        "pipeline_user": "sw23",
        "pipeline_passwd": "fake",
        "pipeline_hostname": "localhost",
        "pipeline_db_name": "aperature",
        "columns": { "vehicle_number": { "max": "NA", "min": 0 }, "maximum_speed" : {"max" : 150, "min" : 0}, "service_date" : {"max" : "NA", "min" : "1990-01-01"} }
    }


@pytest.fixture
def empty_config():
    return config

@pytest.fixture
def loaded_config(tmp_path):
    p = tmp_path / "test_config.json"
    p.write_text(json.dumps(MOCK_CONFIG))
    config.load(p)
    return config
    
def test_get_set_config(empty_config):
    config.set_value("test", 5)
    assert config.get_value("test") == 5

def test_ingest_env(monkeypatch, empty_config):
    monkeypatch.setenv("PIPELINE_USER", "test_user")
    monkeypatch.setenv("PIPELINE_PASSWD", "test_pass")
    empty_config._ingest_env()

    assert empty_config.get_value("pipeline_user") == "test_user"
    assert empty_config.get_value("pipeline_passwd") == "test_pass"

def test_get_set_loaded_config(loaded_config):
    config.set_value("test", 5)
    assert config.get_value("test") == 5
    
    assert config.get_value("pipeline_user") == "sw23"

def test_is_date(empty_config):
    assert config._is_date('2010-01-01')
    assert not config._is_date('10-01-01')
    assert not config._is_date('201k-01-01')
    assert not config._is_date('01-01')

def test_is_na(empty_config):
    assert config._is_na('na')
    assert config._is_na('NA')
    assert config._is_na('')
    assert not config._is_na(3)
    assert not config._is_na(3.2)
    assert not config._is_na('2010-02-02')

def test_check_bounds(loaded_config):
    assert loaded_config.check_bounds("vehicle_number", 2) == BoundsResult.VALID
    
    assert loaded_config.check_bounds("maximum_speed", 180) == BoundsResult.MAX_ERROR
    assert loaded_config.check_bounds("maximum_speed", -1) == BoundsResult.MIN_ERROR

    good_date_str = '2011-01-03'
    bad_date_str = '1970-01-03'

    assert loaded_config.check_bounds("service_date", good_date_str) == BoundsResult.VALID
    assert loaded_config.check_bounds("service_date", bad_date_str) == BoundsResult.MIN_ERROR


