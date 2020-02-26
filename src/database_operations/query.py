import pandas
from sqlalchemy import create_engine

###############################################################################
# "Public" functions

def entire_ctran_table(engine):
    return pandas.read_sql("SELECT * FROM ctran_data;", engine, index_col="data_row")


# NOTE: for processing the table, specify 'chunksize' and see Pandas.read_sql
# documentation.

