import io
import datetime
import pytest
import pandas
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from src.tables import Flagged_Data
from enum import IntEnum
import flaggers.flagger as flagger

@pytest.fixture
def instance_fixture():
    return Flagged_Data("sw23", "invalid", "localhost", "aperture")

@pytest.fixture
def dummy_engine():
    user = "sw23"
    passwd = "invalid"
    hostname = "localhost"
    db_name = "idk_something"
    engine_info = "".join(["postgresql://", user, ":", passwd, "@", hostname, "/", db_name])
    return create_engine(engine_info), user, passwd, hostname, db_name

@pytest.fixture
def mock_connection():
    class mock_connection():
        def __init__(self):
            self.sql = None
        def __enter__(self):
            return self
        def __exit__(self, type, value, traceback):
            return
        def execute(self, sql):
            print(sql)
            self.sql = sql

    return mock_connection()


def test_constructor_build_engine(dummy_engine):
    expected, user, passwd, hostname, db_name = dummy_engine
    instance = Flagged_Data(user, passwd, hostname, db_name)
    assert instance._engine.url == expected.url

def test_constructor_given_engine(dummy_engine):
    engine = dummy_engine[0]
    engine_url = engine.url
    instance = Flagged_Data(engine=engine_url)
    assert instance._engine.url == engine.url

def test_index_col(instance_fixture):
    assert instance_fixture._index_col is None

def test_table_name(instance_fixture):
    assert instance_fixture._table_name == "flagged_data"

def test_expected_cols(instance_fixture):
    expected_cols = ["row_id", "service_key", "flag_id", "service_date"]
    assert instance_fixture._expected_cols == expected_cols

def test_creation_sql(instance_fixture):
    # This tabbing is not accidental.
    expected = "".join(["""
            CREATE TABLE IF NOT EXISTS """, instance_fixture._schema, ".", instance_fixture._table_name, """
            (
                row_id INTEGER,
                service_key INTEGER REFERENCES """, instance_fixture._schema, """.service_periods(service_key),
                flag_id INTEGER REFERENCES """, instance_fixture._schema, """.flags(flag_id) ON UPDATE CASCADE,
                service_date DATE NOT NULL,
                PRIMARY KEY (flag_id, service_key, row_id)
            );"""])
    assert expected == instance_fixture._creation_sql

def test_get_latest_day(mock_connection, instance_fixture):
    instance_fixture._engine.connect = lambda: mock_connection

    expected = "".join(["SELECT MAX(service_date) ",
                       "FROM ", instance_fixture._schema, ".", instance_fixture._table_name,
                       ";"])
    instance_fixture.get_latest_day()
    assert mock_connection.sql == expected

def test_delete_date_range_happy(mock_connection, instance_fixture):
    instance_fixture._engine.connect = lambda: mock_connection
    input_date = "2020/1/1"
    expected = "".join(["DELETE FROM ", instance_fixture._schema, ".", instance_fixture._table_name,
                       " WHERE service_date IN ('", input_date, "', '", input_date, "');"])
    instance_fixture.delete_date_range(input_date)
    assert mock_connection.sql == expected

def test_delete_date_range_bad_engine(instance_fixture):
    instance_fixture._engine = None
    assert instance_fixture.delete_date_range("2020/1/1") == False

def test_delete_date_range_invalid_inputs(instance_fixture):
    def custom_process_dates(start_date, end_date):
        return None, None
    instance_fixture._process_dates = custom_process_dates
    assert instance_fixture.delete_date_range("2020/1/1") == False

def test_delete_date_range_bad_connection(instance_fixture):
    # Since the default engine is already terrible, no changes are needed.
    with pytest.raises(OperationalError):
        instance_fixture.delete_date_range("2020/1/1")

def test_get_date_range(instance_fixture):
    assert instance_fixture._get_date_range("2020/1/1") == [datetime.datetime(2020, 1, 1, 0, 0)]
    assert instance_fixture._get_date_range("2020/1/28", "2020/2/2") == \
            [datetime.datetime(2020, 1, 28, 0, 0),
            datetime.datetime(2020, 1, 29, 0, 0),
            datetime.datetime(2020, 1, 30, 0, 0),
            datetime.datetime(2020, 1, 31, 0, 0),
            datetime.datetime(2020, 2, 1, 0, 0),
            datetime.datetime(2020, 2, 2, 0, 0)]

def test_process_dates(instance_fixture):
    assert instance_fixture._process_dates(None) == \
        (None, None)

    assert instance_fixture._process_dates("2020/1/1") == \
        (datetime.datetime(2020, 1, 1, 0, 0), datetime.datetime(2020, 1, 1, 0, 0))

    assert instance_fixture._process_dates("2020/1/1", "2019/12/31") == \
        (datetime.datetime(2019, 12, 31, 0, 0), datetime.datetime(2020, 1, 1, 0, 0))

    assert instance_fixture._process_dates(datetime.datetime(2019, 12, 31, 0, 0)) == \
        (datetime.datetime(2019, 12, 31, 0, 0), datetime.datetime(2019, 12, 31, 0, 0))

def test_create_view(monkeypatch, instance_fixture):
    class mock_connection():
        def __enter__(self):
            return self
        def __exit__(self, type, value, traceback):
            return
        def execute(self, sql):
            self.sql = sql

    class mock_flag(IntEnum):
        test = 1

    mock = mock_connection()
    instance_fixture._engine.connect = lambda: mock
    monkeypatch.setitem(flagger.flag_descriptions, mock_flag.test, "test")

    expected = "".join([
        "CREATE VIEW ", instance_fixture._schema, ".view_test AS\n",
        "SELECT * FROM ", instance_fixture._schema, ".", instance_fixture._table_name,
        " WHERE flag_id=1;"
    ])
    instance_fixture.create_view_for_flag(mock_flag.test)
    assert mock.sql == expected
