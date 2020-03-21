from .table import Table

class Flagged_Data(Table):

    def __init__(self, user=None, passwd=None, hostname="localhost", db_name="aperture", verbose=False, engine=None):
        super().__init__(user, passwd, hostname, db_name, verbose, engine)
        self._table_name = "flagged_data"
        self._index_col = None
        self._expected_cols = set([
            "flag_id",
            "data_row"
        ])
        self._creation_sql = "".join(["""
            CREATE TABLE IF NOT EXISTS """, self._schema, ".", self._table_name, """
            (
                flag_id INTEGER,
                data_row INTEGER,
                PRIMARY KEY (flag_id, data_row)
            );"""])
