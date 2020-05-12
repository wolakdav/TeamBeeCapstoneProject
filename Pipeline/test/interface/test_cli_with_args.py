import argparse

import pytest

from src.client import _Client
from src.interface import ArgInterface


# @pytest.fixture
# def ctran():
#     return CTran_Data(user="sw23", passwd="fake", hostname="localhost", db_name="aperture", schema="aperture", verbose=True)
#
#
# def test_db(ctran):
#     ai = ArgInterface()
#     df = ai.query_with_args(ctran, ['--date-start=2019-03-01', '--date-end=2019-03-01'])
#     assert len(df.index) == 71084

@pytest.fixture
def cl():
    return _Client()


@pytest.fixture
def ai():
    return ArgInterface()

# TEST RANGE QUERYING

# def test_db(ctran):
#     ai = ArgInterface()
#     df = ai.query_with_args(ctran, None, ['--date-start=2019-03-01', '--date-end=2019-03-01'])
#     assert df is not None
#     assert len(df.index) == 71084

def test_range_no_cl_args_fails(ai):
    with pytest.raises(SystemExit) as sys_ext:
        ai._parse_cl_args(None)
    assert sys_ext.value.code == 2


def test_range_one_garbage_cl_arg_fails(ai):
    with pytest.raises(SystemExit) as sys_ext:
        ai._parse_cl_args(['t'])
    assert sys_ext.value.code == 2


def test_range_two_garbage_cl_args_fails(ai):
    with pytest.raises(SystemExit) as sys_ext:
        ai._parse_cl_args(['t', 'u'])
    assert sys_ext.value.code == 2


def test_range_one_empty_cl_arg_fails(ai):
    with pytest.raises(SystemExit) as sys_ext:
        ai._parse_cl_args(['--date-start='])
    assert sys_ext.value.code == 2


def test_range_one_improper_cl_arg_fails(ai):
    with pytest.raises(SystemExit) as sys_ext:
        ai._parse_cl_args(['--date-start=202'])
    assert sys_ext.value.code == 2


def test_range_one_proper_cl_arg_fails(ai):
    with pytest.raises(SystemExit) as sys_ext:
        ai._parse_cl_args(['--date-start=2020-01-01'])
    assert sys_ext.value.code == 2


def test_range_one_proper_one_improper_cl_arg_fails(ai):
    with pytest.raises(SystemExit) as sys_ext:
        ai._parse_cl_args(['--date-start=2020-01-01', '--date-end=2020-01-'])
    assert sys_ext.value.code == 2


def test_range_two_proper_cl_args_succeeds(ai):
    ai._parse_cl_args(['--date-start=2020-01-01', '--date-end=2020-01-02'])


# TEST ROW QUERYING


def test_row_only_select_arg_fails(ai):
    with pytest.raises(SystemExit) as sys_ext:
        ai._parse_cl_args(['-s'])
    assert sys_ext.value.code == 2


def test_row_two_row_arg_without_value_fails(ai):
    with pytest.raises(SystemExit) as sys_ext:
        ai._parse_cl_args(['-s', '-r'])
    assert sys_ext.value.code == 2


def test_row_two_row_arg_with_wrong_value_fails(ai):
    with pytest.raises(SystemExit) as sys_ext:
        ai._parse_cl_args(['-s', '-r=a'])
    assert sys_ext.value.code == 2


def test_row_two_only_row_arg_fails(ai):
    with pytest.raises(SystemExit) as sys_ext:
        ai._parse_cl_args(['-s', '-r=1'])
    assert sys_ext.value.code == 2


def test_row_two_year_arg_without_value_fails(ai):
    with pytest.raises(SystemExit) as sys_ext:
        ai._parse_cl_args(['-s', '-r=1', '-y'])
    assert sys_ext.value.code == 2


def test_row_two_year_arg_with_wrong_value_fails(ai):
    with pytest.raises(SystemExit) as sys_ext:
        ai._parse_cl_args(['-s', '-r=1', '-y=20'])
    assert sys_ext.value.code == 2


def test_row_two_only_row_and_year_arg_fails(ai):
    with pytest.raises(SystemExit) as sys_ext:
        ai._parse_cl_args(['-s', '-r=1', '-y=2019'])
    assert sys_ext.value.code == 2


def test_row_two_period_arg_without_value_fails(ai):
    with pytest.raises(SystemExit) as sys_ext:
        ai._parse_cl_args(['-s', '-r=1', '-y=2019', 'p'])
    assert sys_ext.value.code == 2


def test_row_two_period_arg_with_value_out_of_lower_range_fails(ai):
    with pytest.raises(SystemExit) as sys_ext:
        ai._parse_cl_args(['-s', '-r=1', '-y=20', 'p=0'])
    assert sys_ext.value.code == 2


def test_row_two_period_arg_with_value_out_of_upper_range_fails(ai):
    with pytest.raises(SystemExit) as sys_ext:
        ai._parse_cl_args(['-s', '-r=1', '-y=20', 'p=4'])
    assert sys_ext.value.code == 2


def test_row_proper_cl_args_succeeds(ai):
    ai._parse_cl_args(['-s', '-r=1', '-y=2019', "-p=1"])


# TEST FLAG QUERYING


def test_flag_only_select_arg_fails(ai):
    with pytest.raises(SystemExit) as sys_ext:
        ai._parse_cl_args(['-s'])
    assert sys_ext.value.code == 2


def test_flag_two_flag_arg_without_value_fails(ai):
    with pytest.raises(SystemExit) as sys_ext:
        ai._parse_cl_args(['-s', '-f'])
    assert sys_ext.value.code == 2


def test_flag_two_flag_arg_with_wrong_value_fails(ai):
    with pytest.raises(SystemExit) as sys_ext:
        ai._parse_cl_args(['-s', '-f=a'])
    assert sys_ext.value.code == 2


def test_flag_only_flag_arg_succeeds(ai):
    ai._parse_cl_args(['-s', '-f=1'])


def test_flag_limit_arg_with_value_out_of_lower_range_fails(ai):
    with pytest.raises(SystemExit) as sys_ext:
        ai._parse_cl_args(['-s', '-f=1', '-l=-1'])
    assert sys_ext.value.code == 2


def test_flag_limit_arg_with_value_0_fails(ai):
    with pytest.raises(SystemExit) as sys_ext:
        ai._parse_cl_args(['-s', '-f=1', '-l=0'])
    assert sys_ext.value.code == 2


def test_flag_with_limit_arg_succeeds(ai):
    ai._parse_cl_args(['-s', '-f=1', '-l=10'])


# TEST DAILY


def test_daily_succeeds(ai):
    ai._parse_cl_args(['--daily'])
