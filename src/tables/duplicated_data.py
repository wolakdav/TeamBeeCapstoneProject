from src.tables.table import Table

class Duplicated_Data(Table):

    def __init__(self, user=None, passwd=None, hostname="localhost", db_name="aperature", verbose=False, engine=None):
        super().__init__(user, passwd, hostname, db_name, verbose, engine)
        self._schema = "aperature"
        self._index_col = None
        self._table_name = "duplicates"
        self._creation_sql = "".join(["""
            CREATE TABLE IF NOT EXISTS """, self._schema, ".", self._table_name, """
            (
                duplicate_ID INTEGER,
                data_row INTEGER,
                PRIMARY KEY (duplicate_ID, data_row)
            );"""])
