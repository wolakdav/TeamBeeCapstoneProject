from .table import Table

class Flags(Table):

    def __init__(self, user=None, passwd=None, hostname="localhost", db_name="aperature", verbose=False, engine=None):
        super().__init__(user, passwd, hostname, db_name, verbose, engine)
        self._schema = "aperature"
        self._table_name = "flags"
        self._index_col = "flag_id"
        self._expected_cols = set([
            "flag_id",
            "description"
        ])
        self._creation_sql = "".join(["""
            CREATE TABLE IF NOT EXISTS """, self._schema, ".", self._table_name, """
            (
                flag_id INTEGER PRIMARY KEY,
                description VARCHAR(200)
            );"""])
