import abc
import sys
import getpass
import pandas
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine.base import Engine
from src.ios import IOs


""" Extending Table
Subclasses should not alter self._engine in any capacity.
For more, see docs/db_ops.md
"""
class Table(IOs, abc.ABC):

    ###########################################################################
    # Public Methods

    # passwd is not stored as member data, it is destroyed after use.
    def __init__(self, user=None, passwd=None, hostname=None, db_name=None, schema="hive", verbose=False, engine=None):
        self._table_name = None
        self._index_col = None
        super().__init__(verbose)
        self._chunksize = 1000

        if schema is None:
            self._schema = self._prompt("Enter the table's schema: ")
        else:
            self._schema = schema

        if engine is not None:
            self._engine = create_engine(engine)

        else:
            if user is None:
                user = self._prompt("Enter username: ")
            if passwd is None:
                passwd = self._prompt("Enter password: ", hide_input=True)
            if hostname is None:
                hostname = self._prompt("Enter hostname: ")
            if db_name is None:
                db_name = self._prompt("Enter the database's name: ")

            self._build_engine(user, passwd, hostname, db_name)

    #######################################################

    def get_engine(self):
        return self._engine

    #######################################################
    
    def get_full_table(self):
        if not isinstance(self._engine, Engine):
            self._print("ERROR: self._engine is not an Engine, cannot continue.")
            return None

        df = None
        sql = "".join(["SELECT * FROM ", self._schema, ".", self._table_name, ";"])
        self._print(sql)
        
        df = pandas.read_sql(sql, self._engine, index_col=self._index_col)

        if not self._check_cols(df):
            self._print("ERROR: the columns of read data does not match the specified columns.")
            return None

        return df

    #######################################################

    def create_schema(self):
        if not isinstance(self._engine, Engine):
            self._print("ERROR: self._engine is not an Engine, cannot continue.")
            return False

        self._print("Connecting to DB.")
        sql = "".join(["CREATE SCHEMA IF NOT EXISTS ", self._schema, ";"])

        conn = self._engine.connect()
        self._print(sql)
        conn.execute(sql)


        self._print("Done.")
        return True

    #######################################################

    def delete_schema(self):
        if not isinstance(self._engine, Engine):
            self._print("ERROR: self._engine is not an Engine, cannot continue.")
            return False

        self._print("Connecting to DB.")
        sql = "".join(["DROP SCHEMA IF EXISTS ", self._schema, " CASCADE;"])
        
        conn = self._engine.connect()
        self._print(sql)
        conn.execute(sql)

        self._print("Done.")
        return True

    #######################################################
    
    def create_table(self):
        if not isinstance(self._engine, Engine):
            self._print("ERROR: self._engine is not an Engine, cannot continue.")
            return False

        if not self.create_schema():
            self._print("ERROR: failed to create schema, cancelling operation.")
            return False

        self._print("Connecting to DB.")

        conn = self._engine.connect()
        self._print(self._creation_sql)
        conn.execute(self._creation_sql)

        self._print("Done.")
        return True

    #######################################################
    

    def delete_table(self):
        if not isinstance(self._engine, Engine):
            self._print("ERROR: self._engine is not an Engine, cannot continue.")
            return False

        self._print("Connecting to DB.")
        sql = "".join(["DROP TABLE IF EXISTS " + self._schema + "." + self._table_name + ";"])
        
        conn = self._engine.connect()
        self._print(sql)
        conn.execute(sql)


        self._print("Done.")
        return True

    #######################################################

    def print(self, string, obj=None, force=False):
        raise AttributeError("AttributeError: " + self.__class__.__name__ + " has no attribute 'print'")

    #######################################################

    def prompt(self, prompt="", hide_input=False):
        raise AttributeError("AttributeError: " + self.__class__.__name__ + " has no attribute 'prompt'")

    ###########################################################################
    # Protected Methods

    def _write_table(self, df, conflict_columns=None):
        # Write the given dataframe into the database.
        # This method is meant to be called by a subclass.
        # df should be a well formed DataFrame, the subclass should form
        # the DataFrame.
        # conflict_columns should be a list of str values used as primary keys.
        #   if conflict_columns is None, will not do ON CONFLICT.
        #   ON CONFLICT is always set to DO NOTHING. This is to ensure there
        #   are no errors when inserting a duplicate row.
        #
        # TODO: Add an update option to ON CONFLICT.
        # Currently ON CONFLICT only exists to stop postgres from
        # throwing a fit whenever there's a duplicate insert. Would be useful
        # to have an option to overwrite the duplicate data instead.
        # Will be very useful for updating the flags table without dropping
        # the whole thing.

        if not self._table_name:
            self._print("ERROR: _write_table not called by a subclass.")
            return False

        if not isinstance(self._engine, Engine):
            self._print("ERROR: invalid engine.")
            return False

        if not self._check_cols(df):
            self._print("ERROR: the columns of data does not match required columns.")
            return False

        self._print("Writing to table...")

        columns = ", ".join(list(df))
        # (value1, value2, ...), (value1, value2, ...), ...
        values = ", ".join(["{}".format(tuple(row)) 
                            for row in df.values.tolist()])

        sql = "".join(["INSERT INTO ", self._schema, ".", self._table_name,
                       " (", columns, ") VALUES ", values])
        if conflict_columns:
            conflict_columns = "({})".format(
                               ", ".join([s for s in conflict_columns]))
            sql += "".join([" ON CONFLICT ", conflict_columns, " DO NOTHING;"])

        con = self._engine.connect()
        con.execute(sql)

        self._print("Done")
        return True

    #######################################################

    def _check_cols(self, sample_df):
        # Check the columns of input df to make sure it matches what we expect.

        # We may or may not care about the order of the columns. If not, then
        # wrap both sides in set().
        if set(list(sample_df)) != set(self._expected_cols):
            return False

        return True

    #######################################################

    """
    Queries the C-Tran data table using the given SQL query.

    :argument   a SQL query string
    :returns    a DataFrame containing query results, or
                None if an exception occurred.
    """
    def _query_table(self, sql):
        if not isinstance(self._engine, Engine):
            self._print("ERROR: invalid engine.")
            return None

        df = None
        self._print(sql)
        
        df = pandas.read_sql(sql, self._engine, index_col=self._index_col)


        if not self._check_cols(df):
            self._print("ERROR: the columns of read data does not match the specified columns.")
            return None

        return df

    ###########################################################################
    # Private Methods

    def _build_engine(self, user, passwd, hostname, db_name):
        engine_info = ["postgresql://", user, ":", passwd, "@", hostname, "/", db_name]
        self._engine = create_engine("".join(engine_info))
        
        self._print("Your engine has been created: ", self._engine)
        return True
