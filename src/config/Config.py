import sys
import json
import os
from datetime import datetime
from dateutil.parser import parse

from enum import Enum

class BoundsResult(Enum):
    VALID = 1     #value is within range
    MAX_ERROR = 2 #value is greater than MAX
    MIN_ERROR = 3 #value is less than MIN

class Config:
    def __init__(self):
        self._data = {}

    def load(self, filename="./assets/config.json", read_env_data=False, debug=False):
        with open(filename) as f:
            self._data = json.load(f)
        if read_env_data:
            self._ingest_env()

    def _ingest_env(self):
        if "PIPELINE_USER" in os.environ:
            self._data["pipeline_user"] = os.environ["PIPELINE_USER"]
        if "PIPELINE_PASSWD" in os.environ:
            self._data["pipeline_passwd"] = os.environ["PIPELINE_PASSWD"]
        if "PIPELINE_HOSTNAME" in os.environ:
            self._data["pipeline_hostname"] = os.environ["PIPELINE_HOSTNAME"]
        if "PIPELINE_DB_NAME" in os.environ:
            self._data["pipeline_db_name"] = os.environ["PIPELINE_DB_NAME"]

    def _is_date(self, val):
        if len(val) == 10:
            for i in range(len(val)):
                if i == 4 or i == 7:
                    if val[i] != '-':
                        return False
                        
                else:
                    if not val[i].isnumeric():
                        return False
        else:
            return False                
        return True

    def _is_na(self, val):
        if val == 'NA' or val == 'na' or val == '':
            return True
        else:
            return False
    def set_value(self, name, val):
        self._data[name] = val

    def get_value(self, val):
        if val in self._data:
            return self._data[val]

    def check_bounds(self, column_name, val):
        if "date" in column_name:
            val = parse(val)

        if column_name in self._data["columns"]:
            col = self._data["columns"][column_name]

            col_max = None
            col_min = None

            if "date" in column_name:
                if col['max'] != 'NA':
                    col_max = parse(col["max"])
                else:
                    col_max = col['max']
            else:
                col_max = col["max"]

            if "date" in column_name:
                if col['min'] != 'NA':
                    col_min = parse(col["min"])
                else:
                    col_min = col['min']
            else:
                col_min = col["min"]

            if col["max"] != "NA":
                if val > col_max:
                    return BoundsResult.MAX_ERROR

            if col["min"] != "NA":
                if val < col_min:
                    return BoundsResult.MIN_ERROR

            return BoundsResult.VALID

if __name__ == "__main__":
     if len(sys.argv) > 1:
         if (sys.argv[1] == "load"):
             config = Config()
             config.load()
             print("Loaded config data.")
