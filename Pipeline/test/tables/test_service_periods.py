import io
import pytest
import pandas
from sqlalchemy import create_engine
from src.tables import Service_Periods
from datetime import datetime

@pytest.fixture
def instance_fixture():
    return Service_Periods("sw23", "invalid", "localhost", "aperture")

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
    instance = Service_Periods(user, passwd, hostname, db_name)
    assert instance._engine.url == expected.url

def test_constructor_given_engine(dummy_engine):
    engine = dummy_engine[0]
    engine_url = engine.url
    instance = Service_Periods(engine=engine_url)
    assert instance._engine.url == engine.url

def test_index_col(instance_fixture):
    assert instance_fixture._index_col == "service_key"

def test_table_name(instance_fixture):
    assert instance_fixture._table_name == "service_periods"

def test_expected_cols(instance_fixture):
    expected_cols = ["start_date", "end_date"]
    assert instance_fixture._expected_cols == expected_cols

def test_creation_sql(instance_fixture):
    # This tabbing is not accidental.
    expected = "".join(["""
            CREATE TABLE IF NOT EXISTS """, instance_fixture._schema, ".", instance_fixture._table_name, """
            (
                service_key BIGSERIAL PRIMARY KEY,
                start_date DATE NOT NULL,
                end_date DATE NOT NULL,
                UNIQUE (start_date, end_date)
            );"""])
    assert expected == instance_fixture._creation_sql

def test_get_service_period(instance_fixture):
    assert instance_fixture.get_service_period(datetime(2019, 1, 1)) == \
               (datetime(2018, 9, 10), datetime(2019, 1, 9))
    assert instance_fixture.get_service_period(datetime(2019, 1, 10)) == \
               (datetime(2019, 1, 10), datetime(2019, 5, 9))
    assert instance_fixture.get_service_period(datetime(2019, 5, 10)) != \
               (datetime(2019, 1, 10), datetime(2019, 5, 9))
    assert instance_fixture.get_service_period(datetime(2019, 5, 10)) == \
               (datetime(2019, 5, 10), datetime(2019, 9, 9))
    assert instance_fixture.get_service_period(datetime(2010, 12, 25)) == \
               (datetime(2010, 9, 10), datetime(2011, 1, 9))

def test_query_or_insert(monkeypatch, instance_fixture):
    monkeypatch.setattr(instance_fixture, "query", lambda _: 1)
    monkeypatch.setattr(instance_fixture, "insert_one", lambda _: 2)
    assert instance_fixture.query_or_insert(datetime(2000, 1, 1)) == 1

    monkeypatch.setattr(instance_fixture, "query", lambda _: None)
    assert instance_fixture.query_or_insert(datetime(2000, 1, 1)) == 2
    

def test_insert_one(instance_fixture):
    class mock_connection():
        def __enter__(self):
            return self
        def __exit__(self, type, value, traceback):
            return
        def execute(self, sql):
            return type('X', (object,), dict(first=lambda: (sql, 0)))
    instance_fixture._engine.connect = lambda: mock_connection()

    expected = "".join(["INSERT INTO ", instance_fixture._schema, ".",
                        instance_fixture._table_name, " (start_date, end_date)"\
                        " VALUES ('2019-01-10', '2019-05-09') RETURNING service_key;"])

    assert instance_fixture.insert_one(datetime(2019, 3, 1)) == expected
