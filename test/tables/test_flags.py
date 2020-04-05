import io
import pytest
import pandas
from sqlalchemy import create_engine
from src.tables import Flags

@pytest.fixture
def instance_fixture():
    return Flags("sw23", "fake")

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
    instance = Flags(user, passwd, hostname, db_name)
    assert instance._engine.url == expected.url

def test_constructor_given_engine(dummy_engine):
    engine = dummy_engine[0]
    engine_url = engine.url
    instance = Flags(engine=engine_url)
    assert instance._engine.url == engine.url

def test_index_col(instance_fixture):
    assert instance_fixture._index_col == "flag_id"

def test_table_name(instance_fixture):
    assert instance_fixture._table_name == "flags"

def test_expected_cols(instance_fixture):
    expected_cols = set(["description"])
    assert instance_fixture._expected_cols == expected_cols

def test_creation_sql(instance_fixture):
    # This tabbing is not accidental.
    expected = "".join(["""
            CREATE TABLE IF NOT EXISTS """, instance_fixture._schema, ".", instance_fixture._table_name, """
            (
                flag_id INTEGER PRIMARY KEY,
                description VARCHAR(200)
            );"""])
    assert expected == instance_fixture._creation_sql
