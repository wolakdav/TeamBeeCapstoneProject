import pytest
import os
import json
from datetime import datetime
from src.config import Config
from src.config import BoundsResult


MOCK_CONFIG = {
        "email": "test@test.com",
        "pipeline_user": "sw23",
        "pipeline_passwd": "fake",
        "pipeline_hostname": "localhost",
        "pipeline_db_name": "aperature",
        "columns": { "vehicle_number": { "max": "NA", "min": 0 }, "maximum_speed" : {"max" : 150, "min" : 0}, "service_date" : { "min" : "1990-01-01" }, "no_bounds" : {} }
    }

@pytest.fixture
def empty_config():
    config = Config()
    return config

@pytest.fixture
def loaded_config(tmp_path):
    p = tmp_path / "test_config.json"
    p.write_text(json.dumps(MOCK_CONFIG))

    config = Config()
    config.load(p)

    return config
    
def test_get_set_config(empty_config):
    empty_config.set_value("test", 5)
    assert empty_config.get_value("test") == 5

def test_ingest_env(monkeypatch, empty_config):
    monkeypatch.setenv("PIPELINE_USER", "test_user")
    monkeypatch.setenv("PIPELINE_PASSWD", "test_pass")
    empty_config._ingest_env()

    assert empty_config.get_value("pipeline_user") == "test_user"
    assert empty_config.get_value("pipeline_passwd") == "test_pass"

def test_get_set_loaded_config(loaded_config):
    loaded_config.set_value("test", 5)
    assert loaded_config.get_value("test") == 5
    
    assert loaded_config.get_value("pipeline_user") == "sw23"

def test_is_date(empty_config):
    assert empty_config._is_date("2010-01-01")
    assert not empty_config._is_date("201k-01-01")    
    assert not empty_config._is_date("notadate")  
    assert not empty_config._is_date("not-a-date")


def test_is_na(empty_config):
    assert empty_config._is_na("na")
    assert empty_config._is_na("n/a")
    assert empty_config._is_na("NA")
    assert empty_config._is_na("N/A")
    assert empty_config._is_na("")
    assert not empty_config._is_na(3)
    assert not empty_config._is_na(3.2)
    assert not empty_config._is_na("2010-02-02")

def test_get_set_bounds(loaded_config):
    assert loaded_config.get_bounds("vehicle_number")["max"] == "NA"
    assert loaded_config.get_bounds("vehicle_number")["min"] == 0
    
    loaded_config.set_bounds("vehicle_number", 200, 400)
    assert loaded_config.get_bounds("vehicle_number")["min"] == 200
    assert loaded_config.get_bounds("vehicle_number")["max"] == 400

    assert loaded_config.check_bounds("vehicle_number", 199) == BoundsResult.MIN_ERROR
    assert loaded_config.check_bounds("vehicle_number", 300) == BoundsResult.VALID
    assert loaded_config.check_bounds("vehicle_number", 401) == BoundsResult.MAX_ERROR

def test_check_bounds(loaded_config):
    assert loaded_config.check_bounds("vehicle_number", 2) == BoundsResult.VALID
    
    assert loaded_config.check_bounds("maximum_speed", 180) == BoundsResult.MAX_ERROR
    assert loaded_config.check_bounds("maximum_speed", -1) == BoundsResult.MIN_ERROR
    
    assert loaded_config.check_bounds("no_bounds", 10000) == BoundsResult.VALID
    assert loaded_config.check_bounds("no_bounds", -10000) == BoundsResult.VALID


    good_date_str = "2011-01-03"
    bad_date_str = "1970-01-03"

    assert loaded_config.check_bounds("service_date", good_date_str) == BoundsResult.VALID
    assert loaded_config.check_bounds("service_date", bad_date_str) == BoundsResult.MIN_ERROR

def test_save_config(loaded_config, tmp_path):
    p = tmp_path / "new_config.json"

    loaded_config.set_value('savetest', 'test')
    loaded_config.set_bounds('savetestbounds', 0, 100)
    loaded_config.save(p)
 
    loaded_config.load(p)
    assert loaded_config.get_value('savetest') == 'test'
    assert loaded_config.get_bounds('savetestbounds')['min'] == 0
    assert loaded_config.get_bounds('savetestbounds')['max'] == 100

    return loaded_config

