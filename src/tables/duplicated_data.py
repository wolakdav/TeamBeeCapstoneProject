from src.tables.table import Table

class Duplicated_Data(Table):

    def __init__(self, user=None, passwd=None, hostname="localhost", db_name="aperature", verbose=False, engine=None):
        super().__init__(user, passwd, hostname, db_name, verbose, engine)
        self._schema = "aperature"
        self._table_name = "duplicates"
        self._index_col = None
        self._expected_cols = [
            "duplicate_id",
            "data_row"
        ]
        self._creation_sql = "".join(["""
            CREATE TABLE IF NOT EXISTS """, self._schema, ".", self._table_name, """
            (
                duplicate_id INTEGER,
                data_row INTEGER,
                PRIMARY KEY (duplicate_id, data_row)
            );"""])
