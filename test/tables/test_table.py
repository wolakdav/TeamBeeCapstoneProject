import io
import pytest
import pandas
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.exc import OperationalError
from src.tables import Table

g_is_valid = None
g_expected = None

# Test_Dummy is used to allow for easy and precise tests of Table.
class Table_Dummy(Table):
    def __init__(self, user=None, passwd=None, hostname=None, db_name=None, schema="hive", verbose=False, engine=None):
        super().__init__(user, passwd, hostname, db_name, schema, verbose, engine)
        self._table_name = "fake"
        self._index_col = "fake_key"
        self._expected_cols = [
            "this",
            "is",
            "a",
            "fake",
            "table"
        ]
        self._creation_sql = "".join(["""
            CREATE TABLE IF NOT EXISTS """, self._schema, ".", self._table_name, """
            (
                fake_key BIGSERIAL PRIMARY KEY,
                this SMALLINT,
                is SMALLINT,
                a SMALLINT,
                fake SMALLINT,
                table SMALLINT
            );"""])


@pytest.fixture
def instance_fixture():
    return Table_Dummy("sw23", "invalid", "localhost", "aperture")

@pytest.fixture
def dummy_engine():
    user = "sw23"
    passwd = "invalid"
    hostname = "localhost"
    db_name = "idk_something"
    engine_info = "".join(["postgresql://", user, ":", passwd, "@", hostname, "/", db_name])
    return create_engine(engine_info), user, passwd, hostname, db_name

@pytest.fixture
def sample_df(instance_fixture):
    test_list = [["a", "b", "c", "d", "e"], ["AA", "BB", "CC", "DD", "EE"]]
    sample_df = pandas.DataFrame(test_list, columns=list(instance_fixture._expected_cols))
    return sample_df

@pytest.fixture
def custom_read_sql(sample_df, instance_fixture):
    def read_sql(sql, engine, index_col):
        expected_sql = "".join(["SELECT * FROM ", instance_fixture._schema, ".", instance_fixture._table_name, ";"])
        if sql != expected_sql:
            return pandas.DataFrame()
        if not isinstance(engine, Engine) or engine.url != instance_fixture._engine.url:
            return pandas.DataFrame()
        if index_col != instance_fixture._index_col:
            return pandas.DataFrame()
        return sample_df

    return read_sql

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
    instance = Table_Dummy(user, passwd, hostname, db_name)
    assert instance._engine.url == expected.url

def test_constructor_given_engine(dummy_engine):
    engine = dummy_engine[0]
    engine_url = engine.url
    instance = Table_Dummy(engine=engine_url)
    assert instance._engine.url == engine.url

def test_no_print(instance_fixture):
    with pytest.raises(AttributeError):
        assert instance_fixture.print("string")

def test_no_prompt(instance_fixture):
    with pytest.raises(AttributeError):
        assert instance_fixture.prompt("string")

def test_chunksize(instance_fixture):
    chunksize = instance_fixture._chunksize
    assert isinstance(chunksize, int) and chunksize > 1

def test_index_col(instance_fixture):
    assert instance_fixture._index_col == "fake_key"

def test_table_name(instance_fixture):
    assert instance_fixture._table_name == "fake"

def test_schema(instance_fixture):
    assert instance_fixture._schema == "hive"

def test_expected_cols(instance_fixture):
    expected_cols = ["this", "is", "a", "fake", "table"]
    assert instance_fixture._expected_cols == expected_cols

def test_creation_sql(instance_fixture):
    # This tabbing is not accidental.
    expected = "".join(["""
            CREATE TABLE IF NOT EXISTS """, instance_fixture._schema, ".", instance_fixture._table_name, """
            (
                fake_key BIGSERIAL PRIMARY KEY,
                this SMALLINT,
                is SMALLINT,
                a SMALLINT,
                fake SMALLINT,
                table SMALLINT
            );"""])
    assert expected == instance_fixture._creation_sql

def test_get_engine(instance_fixture):
    assert instance_fixture.get_engine().url == instance_fixture._engine.url

def test_print_unverbose(capsys, instance_fixture):
    instance_fixture.verbose = False
    instance_fixture._print("Hello!")
    assert capsys.readouterr().out == ""

def test_check_cols_happy(sample_df, instance_fixture):
    assert instance_fixture._check_cols(sample_df) == True

def test_check_cols_sad(instance_fixture):
    instance_fixture._check_cols(pandas.DataFrame())

def test_get_full_table_happy(monkeypatch, custom_read_sql, instance_fixture):
    monkeypatch.setattr("pandas.read_sql", custom_read_sql)
    assert isinstance(instance_fixture.get_full_table(), pandas.DataFrame)

def test_get_full_table_bad_engine(instance_fixture):
    instance_fixture._engine = None
    assert instance_fixture.get_full_table() is None

def test_get_full_table_read_sql_fail(monkeypatch, custom_read_sql, instance_fixture):
    monkeypatch.setattr("pandas.read_sql", custom_read_sql)
    instance_fixture._engine = None
    assert instance_fixture.get_full_table() is None

def test_get_full_table_mismatch_cols(monkeypatch, custom_read_sql, instance_fixture):
    monkeypatch.setattr("pandas.read_sql", custom_read_sql)
    instance_fixture._expected_cols = set([])
    assert instance_fixture.get_full_table() is None

def test_get_full_table_sqlalchemy_error(instance_fixture):
    # Since this table is fake, SQLalchemy will not be able to find it, which
    # will cause this to fail.
    
    with pytest.raises(OperationalError):
        instance_fixture.get_full_table()

def test_get_full_table_read_sql_exception(monkeypatch, instance_fixture):
    def custom_read_sql(sql, engine, index_col):
        raise KeyError

    monkeypatch.setattr("pandas.read_sql", custom_read_sql)
    with pytest.raises(KeyError):
        instance_fixture.get_full_table()

def test_create_schema_verify_sql(custom_connect, instance_fixture):
    global g_is_valid
    global g_expected
    g_expected = "".join(["CREATE SCHEMA IF NOT EXISTS ", instance_fixture._schema, ";"])
    instance_fixture._engine.connect = custom_connect
    assert instance_fixture.create_schema() == True
    assert g_is_valid == True

def test_create_schema_sqlalchemy_error(instance_fixture):
    # Since this table is fake, SQLalchemy will not be able to find it, which
    # will cause this to fail.
    with pytest.raises(OperationalError):
        assert instance_fixture.create_schema() == False

def test_create_schema_bad_engine(instance_fixture):
    instance_fixture._engine = None
    assert instance_fixture.create_schema() == False

def test_delete_schema_verify_sql(custom_connect, instance_fixture):
    global g_is_valid
    global g_expected
    g_expected = "".join(["DROP SCHEMA IF EXISTS ", instance_fixture._schema, " CASCADE;"])
    instance_fixture._engine.connect = custom_connect
    assert instance_fixture.delete_schema() == True
    assert g_is_valid == True

def test_delete_schema_sqlalchemy_error(instance_fixture):
    # Since this table is fake, SQLalchemy will not be able to find it, which
    # will cause this to fail.
    with pytest.raises(OperationalError):
        instance_fixture.delete_schema()

def test_delete_schema_bad_engine(instance_fixture):
    instance_fixture._engine = None
    assert instance_fixture.delete_schema() == False

def test_create_table_verify_sql(custom_connect, instance_fixture):
    global g_is_valid
    global g_expected
    g_expected = instance_fixture._creation_sql
    instance_fixture._engine.connect = custom_connect
    assert instance_fixture.create_table() == True
    assert g_is_valid == True

def test_create_table_schema_fails(instance_fixture):
    # Since the engine contains logic errors, it will pass the
    # isinstance(Engine) check, but create_schema will fail during the
    # credentials check.
    with pytest.raises(OperationalError):
        assert instance_fixture.create_table() == False

def test_create_table_bad_engine(instance_fixture):
    instance_fixture._engine = None
    assert instance_fixture.create_table() == False

def test_create_table_sqlalchemy_error(instance_fixture):
    instance_fixture.create_schema = lambda: True

    with pytest.raises(OperationalError):
        instance_fixture.create_table()

def test_delete_table_verify_sql(custom_connect, instance_fixture):
    global g_is_valid
    global g_expected
    g_expected = "".join(["DROP TABLE IF EXISTS " + instance_fixture._schema + "." + instance_fixture._table_name + ";"])
    instance_fixture._engine.connect = custom_connect
    assert instance_fixture.delete_table() == True
    assert g_is_valid == True

def test_delete_table_bad_engine(instance_fixture):
    instance_fixture._engine = None
    assert instance_fixture.delete_table() == False

def test_delete_table_sqlalchemy_error(instance_fixture):
    # Since this table is fake, SQLalchemy will not be able to find it, which
    # will cause this to fail.
    with pytest.raises(OperationalError):
        instance_fixture.delete_table()


def test_write_table(monkeypatch, instance_fixture):
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

    mock = mock_connection()
    instance_fixture._expected_cols = ["col1", "col2"]
    conflict_columns = ["col1"]
    df = pandas.DataFrame([[1, 2], [3, 4]], columns=instance_fixture._expected_cols)

    instance_fixture._engine.connect = lambda: mock
    instance_fixture._check_cols = lambda _: True

    expected = "".join(["INSERT INTO ", instance_fixture._schema, ".",
                        instance_fixture._table_name, " (col1, col2)"\
                        " VALUES (1, 2), (3, 4) ON CONFLICT (col1) DO NOTHING;"])

    instance_fixture._write_table(df, conflict_columns=conflict_columns)
    assert mock.sql == expected
