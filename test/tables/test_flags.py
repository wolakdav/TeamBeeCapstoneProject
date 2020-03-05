import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from src.tables.flags import Flags

###############################################################################
# Fixtures

@pytest.fixture
def instance():
    return Flags(user="fake_user", passwd="fake_passwd")

@pytest.fixture
def engine_instance():
    test_engine = create_engine("postgresql://winnie-the-pooh:honey@localhost/bee_colonies")
    return [Flags(engine=test_engine.url), test_engine]


###############################################################################
# Constructor tests

def test_passwd_unset(instance):
    assert instance._passwd is None, "Flags._passwd is not unset."

def test_verbose_bool(instance):
    assert isinstance(instance.verbose, bool), "Flags.verbose msut be a boolean."

def test_chunksize_int(instance):
    assert isinstance(instance._chunksize, int), "Flags._chunksize must be an int."

def test_built_engine(instance):
    assert isinstance(instance._engine, Engine), "Flags._engine is not a SQLAlchemy Engine."

def test_schema(instance):
    assert isinstance(instance._schema, str), "Flags._schema must be a str."
    assert len(instance._schema) > 1, "Flags.schema cannot be an empty string."

def test_table_name(instance):
    assert isinstance(instance._table_name, str), "Flags._table_name must be a str."
    assert len(instance._table_name) > 1, "Flags.table_name cannot be an empty string."

def test_index_col(instance):
    assert isinstance(instance._index_col, str), "Flags._index_col must be a str."
    assert instance._index_col == "flag_id", "Flags._index_col has an unexpected str."

def test_expected_cols(instance):
    assert isinstance(instance._expected_cols, list), "Flags._expected_cols must be a list of strs."
    for element in instance._expected_cols:
        assert isinstance(element, str), "Flags._expected_cols must be a list of strs."


def test_engine_copy(engine_instance):
    instance = engine_instance[0]
    engine = engine_instance[1]
    assert isinstance(instance._engine, Engine), "Flags._engine is not a SQLAlchemy Engine."
    assert instance._engine.url == engine.url, "Engine URL was not correctly applied."

def test_compare_instances(instance, engine_instance):
    msg = " does not match between instances that are given user/passwd vs an engine URL."
    alt = engine_instance[0]
    assert instance._schema == alt._schema, "".join(["Flags._schema", msg])
    assert instance._table_name == alt._table_name, "".join(["Flags._table_name", msg])
    assert instance._index_col == alt._index_col, "".join(["Flags._index_col", msg])
    assert instance._expected_cols == alt._expected_cols, "".join(["Flags._expected_cols", msg])
    assert instance._creation_sql == alt._creation_sql, "".join(["Flags._creation_sql", msg])
