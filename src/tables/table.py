""" Perform assumption checking
# TODO: send this a faulty engine, and one without permissions
# TODO: see what exceptions can be thrown by conn
# exception: psycopg2.errors.AdminShutdown
# exception: sqlalchemy.exc.OperationalError
"""
# TODO: make sure things return bools as appropriate
import abc
import getpass
import pandas
from sqlalchemy import create_engine

class Table(abc.ABC):
    """ Subclasses should declare/initialize:
    str self._table_name
    str self._index_col
    str self._creation_sql
    str self._schema
    """

    ###########################################################################
    # Public Methods

    def __init__(self, user=None, passwd=None, hostname="localhost", db_name="aperature", verbose=False):
        self.verbose = verbose
        self._user = None
        self._passwd = None
        self._hostname = hostname
        self._chunksize = 1000
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

        self.build_engine()

    #######################################################

    def build_engine(self):
        engine_info = ["postgresql://", self._user, ":", self._passwd, "@", self._hostname, "/", self._db_name]
        self._engine = create_engine("".join(engine_info))
        
        self._print("Your engine has been created: ", self._engine)
        return True

    #######################################################

    def print_engine(self):
        self._print("", self._engine, force=True)

    #######################################################
    
    # TODO: can read_sql throw exceptions (sqlalchemy.exc.ProgrammingError)? or fail to connect?
    # NOTE: if there is no ctran_data table, this will not work, obviously.
    def get_full_table(self):
        sql = "".join(["SELECT * FROM ", self._schema, ".", self._table_name, ";"])
        self._print(sql)
        return pandas.read_sql(sql, self._engine, index_col=self._index_col)

    #######################################################

    def create_schema(self):
        self._print("Connecting to DB.")
        with self._engine.connect() as conn:
            sql = "".join(["CREATE SCHEMA IF NOT EXISTS ", self._schema, ";"])
            self._print(sql)
            conn.execute(sql)

        self._print("Done.")
        return True

    #######################################################

    def delete_schema(self):
        self._print("Connecting to DB.")
        with self._engine.connect() as conn:
            sql = "".join(["DROP SCHEMA IF EXISTS ", self._schema, " CASCADE;"])
            self._print(sql)
            conn.execute(sql)

        self._print("Done.")
        return True

    #######################################################
    
    def create_table(self):
        if not self.create_schema():
            self._print("ERROR: failed to create schema, cancelling operation.")
            return False

        self._print("Connecting to DB.")
        with self._engine.connect() as conn:
            self._print(self._creation_sql)
            conn.execute(self._creation_sql)

        self._print("Done.")
        return True

    #######################################################

    # TODO: catch that invalid SQL exception or invalid table name, and return false
    # or if the table already exists - sqlalchemy.exc.ProgrammingError
    def delete_table(self):
        self._print("Connecting to DB.")
        with self._engine.connect() as conn:
            sql = "".join(["DROP TABLE IF EXISTS " + self._schema + "." + self._table_name + ";"])
            self._print(sql)
            conn.execute(sql)

        self._print("Done.")
        return True

    ###########################################################################
    # Private Methods

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
