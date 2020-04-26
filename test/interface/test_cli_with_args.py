import argparse

import pytest
from src.interface import ArgInterface
from src.tables import CTran_Data


# @pytest.fixture
# def ctran():
#     return CTran_Data(verbose=True)
#
# def test_db(ctran):
#     ai = ArgInterface()
#     df = ai.query_with_args(ctran, ['--date-start=2019-03-01', '--date-end=2019-03-01'])
#     assert len(df.index) == 71084
@pytest.fixture
def ai():
    return ArgInterface()

def test_no_cl_args_fails(ai):
    with pytest.raises(SystemExit) as sys_ext:
        ai._parse_cl_args(None)
    assert sys_ext.value.code == 2

def test_one_garbage_cl_arg_fails(ai):
    with pytest.raises(SystemExit) as sys_ext:
        ai._parse_cl_args(['t'])
    assert sys_ext.value.code == 2

def test_two_garbage_cl_args_fails(ai):
    with pytest.raises(SystemExit) as sys_ext:
        ai._parse_cl_args(['t', 'u'])
    assert sys_ext.value.code == 2

def test_one_empty_cl_arg_fails(ai):
    with pytest.raises(SystemExit) as sys_ext:
        ai._parse_cl_args(['--date-start='])
    assert sys_ext.value.code == 2

def test_one_improper_cl_arg_fails(ai):
    with pytest.raises(SystemExit) as sys_ext:
        ai._parse_cl_args(['--date-start=202'])
    assert sys_ext.value.code == 2

def test_one_proper_cl_arg_fails(ai):
    with pytest.raises(SystemExit) as sys_ext:
        ai._parse_cl_args(['--date-start=2020-01-01'])
    assert sys_ext.value.code == 2

def test_one_proper_one_improper_cl_arg_fails(ai):
    with pytest.raises(SystemExit) as sys_ext:
        ai._parse_cl_args(['--date-start=2020-01-01', '--date-end=2020-01-'])
    assert sys_ext.value.code == 2

def test_two_proper_cl_args_succeeds(ai):
    ai._parse_cl_args(['--date-start=2020-01-01', '--date-end=2020-01-02'])



