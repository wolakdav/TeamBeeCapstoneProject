import io
import pytest
import pandas
from sqlalchemy import create_engine
from src.tables import Service_Periods

@pytest.fixture
def service_periods_fixture():
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

def test_verbose(service_periods_fixture):
    verbose = service_periods_fixture.verbose
    assert isinstance(verbose, bool) and verbose == False

def test_chunksize(service_periods_fixture):
    chunksize = service_periods_fixture._chunksize
    assert isinstance(chunksize, int) and chunksize > 1

def test_index_col(service_periods_fixture):
    assert service_periods_fixture._index_col == "service_key"

def test_table_name(service_periods_fixture):
    assert service_periods_fixture._table_name == "service_periods"

def test_schema(service_periods_fixture):
    assert service_periods_fixture._schema == "hive"

def test_expected_cols(service_periods_fixture):
    expected_cols = set(["month", "year", "ternary"])
    assert service_periods_fixture._expected_cols == expected_cols

def test_creation_sql(service_periods_fixture):
    # This tabbing is not accidental.
    expected = "".join(["""
            CREATE TABLE IF NOT EXISTS """, service_periods_fixture._schema, ".", service_periods_fixture._table_name, """
            (
                service_key BIGSERIAL PRIMARY KEY,
                month SMALLINT NOT NULL CHECK ( (month <= 12) AND (month >= 1) ),
                year SMALLINT NOT NULL CHECK (year > 1700),
                ternary SMALLINT NOT NULL CHECK ( (ternary <= 3) AND (ternary >= 1) ),
                UNIQUE (month, year, ternary)
            );"""])
    assert expected == service_periods_fixture._creation_sql

def test_get_engine(service_periods_fixture):
    assert service_periods_fixture.get_engine().url == service_periods_fixture._engine.url

def test_print_unverbose(capsys, service_periods_fixture):
    service_periods_fixture.verbose = False
    service_periods_fixture._print("Hello!")
    assert capsys.readouterr().out == ""

def test_print_no_obj(capsys, service_periods_fixture):
    service_periods_fixture.verbose = True
    service_periods_fixture._print("Hello!")
    assert capsys.readouterr().out == "Hello!\n"

def test_print_no_obj_forced(capsys, service_periods_fixture):
    service_periods_fixture.verbose = False
    service_periods_fixture._print("Hello!", force=True)
    assert capsys.readouterr().out == "Hello!\n"

def test_print_obj(capsys, service_periods_fixture):
    service_periods_fixture.verbose = True
    obj = ["Pizza", "Pie"]
    service_periods_fixture._print("Hello!", obj)
    assert capsys.readouterr().out == "Hello!['Pizza', 'Pie']\n"

def test_print_obj_forced(capsys, service_periods_fixture):
    service_periods_fixture.verbose = False
    obj = ["Pizza", "Pie"]
    service_periods_fixture._print("Hello!", obj, True)
    assert capsys.readouterr().out == "Hello!['Pizza', 'Pie']\n"

def test_prompt_unhidden(capsys, monkeypatch, service_periods_fixture):
    expected = "sw23"
    prompt = "> "
    monkeypatch.setattr("sys.stdin", io.StringIO(expected + "\n"))
    result = service_periods_fixture._prompt(prompt)
    assert result == expected

def test_prompt_hidden(capsys, monkeypatch, service_periods_fixture):
    expected = "fake\n"
    prompt = "> "
    monkeypatch.setattr("getpass.getpass", lambda _: expected)
    result = service_periods_fixture._prompt(prompt, True)
    assert result == expected

def test_check_cols_happy(service_periods_fixture):
    test_list = [["a","b","c"], ["AA","BB","CC"]]
    sample_df = pandas.DataFrame(test_list, columns=list(service_periods_fixture._expected_cols))
    assert service_periods_fixture._check_cols(sample_df) == True

def test_check_cols_sad(service_periods_fixture):
    assert service_periods_fixture._check_cols(pandas.DataFrame()) == False

# TODO: mock out DB and test:
#   get_full_table
#   create_schema
#   delete_schema
#   create_table
#   delete_table


# TODO: When done testing this class, copy and adjust these tests for the other
# classes as well. CTran_Data will need to have custom tests for create_table.
#
# Alternatively, possibly use these tests of inherited Table members/methods to
# be used for all inherited and unchanged members/methods between subclasses.
# This might be taken even further by just having a subclass of Table that
# exists to serve as a testing class for Table, and then just test the
# specifics of each subclass.
