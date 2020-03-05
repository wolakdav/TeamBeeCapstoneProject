import abc
import sys
import getpass
import pandas
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError


""" Subclasses should declare/initialize:
str self._schema
str self._table_name
str self._index_col
    For the purposes of loading via Pandas' index_col parameter.
str list self._expected_cols
    This will contain a list of strings of the columns in the table.
str self._creation_sql

Additionally, subclasses should not alter self._engine in any capacity.
"""
class Table(abc.ABC):

    ###########################################################################
    # Public Methods

    # For security purposes, self._passwd is unset after the engine is created.
    def __init__(self, user=None, passwd=None, hostname="localhost", db_name="aperature", verbose=False, engine=None):
        # Currently, _hostname, _db_name, _user, and _passwd are just used to
        # create the engine. Consequently, if an engine URL is supplied, none
        # of the other data will be filled since their result has been served.
        self.verbose = verbose
        self._chunksize = 1000

        if engine is not None:
            self._engine = create_engine(engine)

        else:
            self._user = None
            self._passwd = None
            self._hostname = hostname
            self._db_name = db_name
            self._engine = None

            if user is None:
                self._user = self._prompt("Enter username: ")
            else:
                self._user = user

            if passwd is None:
                self._passwd = self._prompt("Enter password: ", hide_input=True)
            else:
                self._passwd = passwd

            self._build_engine()
            self._print("Unsetting Table._passwd for security purposes.")
            self._passwd = None

    #######################################################

    def get_engine(self):
        return self._engine

    #######################################################
    
    # NOTE: if there is no ctran_data table, this will not work, obviously.
    def get_full_table(self):
        if self._engine is None:
            self._print("ERROR: self._engine is None, cannot continue.")
            return None

        sql = "".join(["SELECT * FROM ", self._schema, ".", self._table_name, ";"])
        self._print(sql)
        try:
            df = pandas.read_sql(sql, self._engine, index_col=self._index_col)
            return df

        except SQLAlchemyError as error:
            print("SQLAclchemy:", error)
            return None
        except ValueError as error:
            print("Pandas:", error)
            return None

    #######################################################

    def create_schema(self):
        if self._engine is None:
            self._print("ERROR: self._engine is None, cannot continue.")
            return False

        self._print("Connecting to DB.")
        sql = "".join(["CREATE SCHEMA IF NOT EXISTS ", self._schema, ";"])
        try:
            with self._engine.connect() as conn:
                self._print(sql)
                conn.execute(sql)

        except SQLAlchemyError as error:
            print("SQLAclchemy:", error)
            return False

        self._print("Done.")
        return True

    #######################################################

    def delete_schema(self):
        if self._engine is None:
            self._print("ERROR: self._engine is None, cannot continue.")
            return False

        self._print("Connecting to DB.")
        sql = "".join(["DROP SCHEMA IF EXISTS ", self._schema, " CASCADE;"])
        try:
            with self._engine.connect() as conn:
                self._print(sql)
                conn.execute(sql)

        except SQLAlchemyError as error:
            print("SQLAclchemy:", error)
            return False

        self._print("Done.")
        return True

    #######################################################
    
    def create_table(self):
        if self._engine is None:
            self._print("ERROR: self._engine is None, cannot continue.")
            return False

        if not self.create_schema():
            self._print("ERROR: failed to create schema, cancelling operation.")
            return False

        self._print("Connecting to DB.")
        try:
            with self._engine.connect() as conn:
                self._print(self._creation_sql)
                conn.execute(self._creation_sql)

        except SQLAlchemyError as error:
            print("SQLAclchemy:", error)
            return False

        self._print("Done.")
        return True

    #######################################################

    def delete_table(self):
        if self._engine is None:
            self._print("ERROR: self._engine is None, cannot continue.")
            return False

        self._print("Connecting to DB.")
        sql = "".join(["DROP TABLE IF EXISTS " + self._schema + "." + self._table_name + ";"])
        try:
            with self._engine.connect() as conn:
                self._print(sql)
                conn.execute(sql)

        except SQLAlchemyError as error:
            print("SQLAclchemy:", error)
            return False

        self._print("Done.")
        return True

    ###########################################################################
    # Private Methods

    def _build_engine(self):
        engine_info = ["postgresql://", self._user, ":", self._passwd, "@", self._hostname, "/", self._db_name]
        self._engine = create_engine("".join(engine_info))
        
        self._print("Your engine has been created: ", self._engine)
        return True

    #######################################################

    def _prompt(self, prompt="", hide_input=False):
        while True:
            try:
                value = None
                if hide_input:
                    value = getpass.getpass(prompt)
                else:
                    value = input(prompt)
                return value
            except EOFError:
                print()

    #######################################################

    def _print(self, string, obj=None, force=False):
        if not force:
            if not self.verbose:
                return

        if obj is None:
            print(string)

        else:
            print(string, end="")
            print(obj)
