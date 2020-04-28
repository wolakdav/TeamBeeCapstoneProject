from .table import Table

class Flagged_Data(Table):

    def __init__(self, user=None, passwd=None, hostname="localhost", db_name="aperture", verbose=False, engine=None):
        super().__init__(user, passwd, hostname, db_name, verbose, engine)
        self._table_name = "flagged_data"
        self._index_col = None
        self._expected_cols = set([
            "flag_id",
            "row_id"
        ])
        self._creation_sql = "".join(["""
            CREATE TABLE IF NOT EXISTS """, self._schema, ".", self._table_name, """
            (
                flag_id INTEGER REFERENCES """, self._schema, """.flags(flag_id),
                service_key INTEGER REFERENCES """, self._schema, """.service_periods(service_key),
                row_id INTEGER,
                PRIMARY KEY (flag_id, service_key, row_id)
            );"""])

# SELECT fd.flag_id
# FROM
#      aperture.flagged_data AS fd,
#      aperture.service_periods AS sp
# WHERE
#       fd.row_id = '10'
# AND
#       sp.year = '2019'
# AND
#       sp.ternary = '1'
# AND
#       fd.service_key = sp.service_key;
    def query_flags_by_row_id(self, sp_table, row_id, service_year, service_period):
        sql = "".join(["SELECT flag_id FROM ",
                       self._schema,
                       ".",
                       self._table_name,
                       " AS fd, ",
                       self._schema,
                       ".",
                       sp_table,
                       " AS sp, WHERE fd.row_id = '",
                       row_id,
                       "' AND sp.year = '",
                       service_year,
                       "' AND sp.ternary = '",
                       service_period,
                       "' AND fd.service_key = sp.service_key"
                       ";"])

        return self._query_table(sql)

    def query_flags_by_flag_id(self, flag_id, limit):
        sql = "".join(["SELECT flag_id, row_id FROM ",
                       self._schema,
                       ".",
                       self._table_name,
                       " WHERE flag_id = '",
                       flag_id,
                       "' LIMIT '",
                       limit,
                       "';"])

        return self._query_table(sql)
