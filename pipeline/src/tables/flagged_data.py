from pipeline.src.tables.table import Table

class Flagged_Data(Table):

    def __init__(self, user=None, passwd=None, hostname="localhost", db_name="aperature", verbose=False, engine=None):
        super().__init__(user, passwd, hostname, db_name, verbose, engine)
        self._schema = "aperature"
        self._index_col = None
        self._table_name = "flagged_data"
        self._creation_sql = "".join(["""
            CREATE TABLE IF NOT EXISTS """, self._schema, ".", self._table_name, """
            (
                flag_ID INTEGER,
                data_row INTEGER,
                PRIMARY KEY (flag_ID, data_row)
            );"""])
