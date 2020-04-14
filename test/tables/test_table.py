import io
import pytest
import pandas
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from src.tables import Table

g_is_valid = None
g_expected = None

# Test_Dummy is used to allow for easy and precise tests of Table.
class Table_Dummy(Table):
    def __init__(self, user=None, passwd=None, hostname="localhost", db_name="aperture", verbose=False, engine=None):
        super().__init__(user, passwd, hostname, db_name, verbose, engine)
        self._table_name = "fake"
        self._index_col = "fake_key"
        self._expected_cols = set([
            "this",
            "is",
            "a",
            "fake",
            "table"
        ])
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
    return Table_Dummy("sw23", "invalid")

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

def test_verbose(instance_fixture):
    verbose = instance_fixture.verbose
    assert isinstance(verbose, bool) and verbose == False

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
    expected_cols = set(["this", "is", "a", "fake", "table"])
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

def test_print_no_obj(capsys, instance_fixture):
    instance_fixture.verbose = True
    instance_fixture._print("Hello!")
    assert capsys.readouterr().out == "Hello!\n"

def test_print_no_obj_forced(capsys, instance_fixture):
    instance_fixture.verbose = False
    instance_fixture._print("Hello!", force=True)
    assert capsys.readouterr().out == "Hello!\n"

def test_print_obj(capsys, instance_fixture):
    instance_fixture.verbose = True
    obj = ["Pizza", "Pie"]
    instance_fixture._print("Hello!", obj)
    assert capsys.readouterr().out == "Hello!['Pizza', 'Pie']\n"

def test_print_obj_forced(capsys, instance_fixture):
    instance_fixture.verbose = False
    obj = ["Pizza", "Pie"]
    instance_fixture._print("Hello!", obj, True)
    assert capsys.readouterr().out == "Hello!['Pizza', 'Pie']\n"

def test_prompt_unhidden(capsys, monkeypatch, instance_fixture):
    expected = "sw23"
    prompt = "> "
    monkeypatch.setattr("sys.stdin", io.StringIO(expected + "\n"))
    result = instance_fixture._prompt(prompt)
    assert result == expected

def test_prompt_hidden(capsys, monkeypatch, instance_fixture):
    expected = "fake\n"
    prompt = "> "
    monkeypatch.setattr("getpass.getpass", lambda _: expected)
    result = instance_fixture._prompt(prompt, True)
    assert result == expected

def test_check_cols_happy(sample_df, instance_fixture):
    assert instance_fixture._check_cols(sample_df) == True

def test_check_cols_sad(instance_fixture):
    assert instance_fixture._check_cols(pandas.DataFrame()) == False

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
    assert instance_fixture.get_full_table() is None

def test_get_full_table_read_sql_exception(monkeypatch, instance_fixture):
    def custom_read_sql(sql, engine, index_col):
        raise KeyError

    monkeypatch.setattr("pandas.read_sql", custom_read_sql)
    assert instance_fixture.get_full_table() == None

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
    assert instance_fixture.delete_schema() == False

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
    assert instance_fixture.create_table() == False

def test_create_table_bad_engine(instance_fixture):
    instance_fixture._engine = None
    assert instance_fixture.create_table() == False

def test_create_table_sqlalchemy_error(instance_fixture):
    instance_fixture.create_schema = lambda: True
    assert instance_fixture.create_table() == False

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
    assert instance_fixture.delete_table() == False
