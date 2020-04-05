import io
import pytest
import pandas
from sqlalchemy import create_engine
from src.tables import Service_Periods

@pytest.fixture
def instance_fixture():
    return Service_Periods("sw23", "fake")

@pytest.fixture
def dummy_engine():
    user = "sw23"
    passwd = "fake"
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
    expected_cols = set(["month", "year", "ternary"])
    assert instance_fixture._expected_cols == expected_cols

def test_creation_sql(instance_fixture):
    # This tabbing is not accidental.
    expected = "".join(["""
            CREATE TABLE IF NOT EXISTS """, instance_fixture._schema, ".", instance_fixture._table_name, """
            (
                service_key BIGSERIAL PRIMARY KEY,
                month SMALLINT NOT NULL CHECK ( (month <= 12) AND (month >= 1) ),
                year SMALLINT NOT NULL CHECK (year > 1700),
                ternary SMALLINT NOT NULL CHECK ( (ternary <= 3) AND (ternary >= 1) ),
                UNIQUE (month, year, ternary)
            );"""])
    assert expected == instance_fixture._creation_sql
