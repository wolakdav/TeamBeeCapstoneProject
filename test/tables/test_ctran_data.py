import io
import pytest
import pandas
from sqlalchemy import create_engine
from src.tables import CTran_Data

@pytest.fixture
def instance_fixture():
    return CTran_Data("sw23", "invalid")

@pytest.fixture
def dummy_engine():
    user = "sw23"
    passwd = "invalid"
    hostname = "localhost"
    db_name = "idk_something"
    engine_info = "".join(["postgresql://", user, ":", passwd, "@", hostname, "/", db_name])
    return create_engine(engine_info), user, passwd, hostname, db_name


def test_constructor_build_engine(dummy_engine):
    expected, user, passwd, hostname, db_name = dummy_engine
    instance = CTran_Data(user, passwd, hostname, db_name)
    assert instance._engine.url == expected.url

def test_constructor_given_engine(dummy_engine):
    engine = dummy_engine[0]
    engine_url = engine.url
    instance = CTran_Data(engine=engine_url)
    assert instance._engine.url == engine.url

def test_index_col(instance_fixture):
    assert instance_fixture._index_col == "row_id"

def test_table_name(instance_fixture):
    assert instance_fixture._table_name == "ctran_data"

def test_schema(instance_fixture):
    assert instance_fixture._schema == "aperture"

def test_expected_cols(instance_fixture):
    expected_cols = set([
        "service_date",
        "vehicle_number",
        "leave_time",
        "train",
        "route_number",
        "direction",
        "service_key",
        "trip_number",
        "stop_time",
        "arrive_time",
        "dwell",
        "location_id",
        "door",
        "ons",
        "offs",
        "estimated_load",
        "lift",
        "maximum_speed",
        "train_mileage",
        "pattern_distance",
        "location_distance",
        "x_coordinate",
        "y_coordinate",
        "data_source",
        "schedule_status",
        "trip_id"
    ])
    assert instance_fixture._expected_cols == expected_cols

def test_creation_sql(instance_fixture):
    # This tabbing is not accidental.
    expected = "".join(["""
            CREATE TABLE IF NOT EXISTS """, instance_fixture._schema, ".", instance_fixture._table_name, """
            (
                row_id BIGSERIAL PRIMARY KEY,
                service_date DATE,
                vehicle_number INTEGER,
                leave_time INTEGER,
                train INTEGER,
                route_number INTEGER,
                direction SMALLINT,
                service_key CHARACTER(1),
                trip_number INTEGER,
                stop_time INTEGER,
                arrive_time INTEGER,
                dwell INTEGER,
                location_id INTEGER,
                door INTEGER,
                ons INTEGER,
                offs INTEGER,
                estimated_load INTEGER,
                lift INTEGER,
                maximum_speed INTEGER,
                train_mileage FLOAT,
                pattern_distance FLOAT,
                location_distance FLOAT,
                x_coordinate FLOAT,
                y_coordinate FLOAT,
                data_source INTEGER,
                schedule_status INTEGER,
                trip_id INTEGER
            );"""])
    assert expected == instance_fixture._creation_sql

# TODO: test the overridden create_table.
#       verify sql
#       unset engine: returns False
#       invalid cols of result: returns False
#       pandas error: returns False
#           FileNotFoundError
#       check_cols failure: invalid cols of sample data
#       SQLalchemy error: returns False
