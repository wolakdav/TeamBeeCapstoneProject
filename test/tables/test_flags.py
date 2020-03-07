import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine.base import Engine
from src.tables.flags import Flags

###############################################################################
# Fixtures

@pytest.fixture
def instance():
    return Flags(user="fake_user", passwd="fake_passwd")

@pytest.fixture
def engine():
    return create_engine("postgresql://winnie-the-pooh:honey@localhost/bee_colonies")

@pytest.fixture
def engine_instance(engine):
    return Flags(engine=engine.url)


###############################################################################
# Constructor tests

# Aspects of Flag relating to _schema and _table_name are not particularly
# testable apart from type and non-null string as they are designed to be
# highly adjustable as needed, as opposed to _index_col, which is pretty
# static.

def test_passwd_unset(instance):
    assert instance._passwd is None, "Flags._passwd is not unset."

def test_verbose_bool(instance):
    assert isinstance(instance.verbose, bool), "Flags.verbose msut be a boolean."

def test_chunksize_int(instance):
    assert isinstance(instance._chunksize, int), "Flags._chunksize must be an int."
    assert instance._chunksize > 0, "Flags._chunksize must be greater than zero."

def test_built_engine(instance):
    assert isinstance(instance._engine, Engine), "Flags._engine is not a SQLAlchemy Engine."

def test_schema(instance):
    assert isinstance(instance._schema, str), "Flags._schema must be a str."
    assert len(instance._schema) > 0, "Flags.schema cannot be an empty string."

def test_table_name(instance):
    assert isinstance(instance._table_name, str), "Flags._table_name must be a str."
    assert len(instance._table_name) > 0, "Flags.table_name cannot be an empty string."

def test_index_col(instance):
    assert isinstance(instance._index_col, str), "Flags._index_col must be a str."
    assert instance._index_col == "flag_id", "Flags._index_col has an unexpected str."

def test_expected_cols(instance):
    assert isinstance(instance._expected_cols, list), "Flags._expected_cols must be a list of strs."
    for element in instance._expected_cols:
        assert isinstance(element, str), "Flags._expected_cols must be a list of strs."
        assert len(element) > 0, "Flags._expected_cols must contain non-null strs."

def test_engine_copy(engine_instance, engine):
    instance = engine_instance
    assert isinstance(instance._engine, Engine), "Flags._engine is not a SQLAlchemy Engine."
    assert instance._engine.url == engine.url, "Engine URL was not correctly applied."

def test_compare_instances(instance, engine_instance):
    msg = " does not match between instances that are given user/passwd vs an engine URL."
    alt = engine_instance
    assert instance._schema == alt._schema, "".join(["Flags._schema", msg])
    assert instance._table_name == alt._table_name, "".join(["Flags._table_name", msg])
    assert instance._index_col == alt._index_col, "".join(["Flags._index_col", msg])
    assert instance._expected_cols == alt._expected_cols, "".join(["Flags._expected_cols", msg])
    assert instance._creation_sql == alt._creation_sql, "".join(["Flags._creation_sql", msg])


###############################################################################
# Method Tests

def test_get_engine(instance):
    assert isinstance(instance.get_engine(), Engine), "Flags.get_flags_engine() does not return an Engine."

# TODO: figure out how to mock with pytest's monkeypatch or whatever
# get the below working to make sure it works
def test_get_full_table_happy(instance):
    pass

def test_get_full_table_sqlalchemy_exception(instance, engine):
    # engine is fake so it will cause an error.
    instance._engine = engine
    assert instance.get_full_table() is None, "Flags.get_full_table() failed to catch a SQLAlchemy exception."
