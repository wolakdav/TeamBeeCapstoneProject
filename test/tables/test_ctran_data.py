import io
import pytest
import pandas
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from src.tables import CTran_Data

g_is_valid = None
g_expected = None

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

# This fixture uses g_is_valid and g_expected. It will not reset those values
# before or after execution.
@pytest.fixture
def custom_connect():
    class custom_connect():
        def execute(self, sql):
            global g_is_valid
            global g_expected

            if sql != g_expected:
                g_is_valid = False
            else:
                g_is_valid = True

    return custom_connect


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

def test_create_table_bad_engine(instance_fixture):
    instance_fixture._engine = None
    assert instance_fixture.create_table() == False

def test_create_table_bad_filepath(monkeypatch, instance_fixture):
    def custom_read_csv(csv_location, parse_dates):
        raise FileNotFoundError

    monkeypatch.setattr("pandas.read_csv", custom_read_csv)
    assert instance_fixture.create_table() == False

def test_create_table_invalid_cols(monkeypatch, instance_fixture):
    test_list = [["a", "b", "c", "d", "e"], ["AA", "BB", "CC", "DD", "EE"]]
    bad_df = pandas.DataFrame(test_list)
    monkeypatch.setattr("pandas.read_csv", lambda _, parse_dates: bad_df)
    assert instance_fixture.create_table() == False

def test_create_table_helper_fails(monkeypatch, instance_fixture):
    monkeypatch.setattr("pandas.read_csv", lambda _, parse_dates: pandas.DataFrame)
    instance_fixture._check_cols = lambda _: True
    instance_fixture._create_table_helper = lambda _: False
    assert instance_fixture.create_table() == False

# TODO: test the overridden create_table.
#       verify sql
#       if super().create_table failes, then so should create table helper
#       SQLalchemy error: returns False
#       when done, have as happy a test as possible - actually read the file
