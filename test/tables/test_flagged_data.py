import io
import pytest
import pandas
from sqlalchemy import create_engine
from src.tables import Flagged_Data

@pytest.fixture
def service_periods_fixture():
    return Flagged_Data("sw23", "fake")

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
    instance = Flagged_Data(user, passwd, hostname, db_name)
    assert instance._engine.url == expected.url

def test_constructor_given_engine(dummy_engine):
    engine = dummy_engine[0]
    engine_url = engine.url
    instance = Flagged_Data(engine=engine_url)
    assert instance._engine.url == engine.url

def test_index_col(service_periods_fixture):
    assert service_periods_fixture._index_col is None

def test_table_name(service_periods_fixture):
    assert service_periods_fixture._table_name == "flagged_data"

def test_schema(service_periods_fixture):
    assert service_periods_fixture._schema == "hive"

def test_expected_cols(service_periods_fixture):
    expected_cols = set(["flag_id", "row_id"])
    assert service_periods_fixture._expected_cols == expected_cols

def test_creation_sql(service_periods_fixture):
    # This tabbing is not accidental.
    expected = "".join(["""
            CREATE TABLE IF NOT EXISTS """, service_periods_fixture._schema, ".", service_periods_fixture._table_name, """
            (
                flag_id INTEGER REFERENCES """, service_periods_fixture._schema, """.flags(flag_id),
                service_key INTEGER REFERENCES """, service_periods_fixture._schema, """.service_periods(service_key),
                row_id INTEGER,
                PRIMARY KEY (flag_id, service_key, row_id)
            );"""])
    assert expected == service_periods_fixture._creation_sql
