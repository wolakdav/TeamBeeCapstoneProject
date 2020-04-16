import sys
import json
import os
from datetime import datetime
from dateutil.parser import parse, ParserError
from enum import Enum

CONFIG_FILENAME = "./assets/config.json"

class BoundsResult(Enum):
    VALID = 1     #value is within range
    MAX_ERROR = 2 #value is greater than MAX
    MIN_ERROR = 3 #value is less than MIN

class Config:
    def __init__(self):
        self._data = {}
    def load(self, filename=CONFIG_FILENAME, read_env_data=False, debug=False):
        self._filename = filename
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
        if not isinstance(val, str):
            return False
        try:
            parse(val)
        except ParserError:
            return False
            
        return True

    def _is_na(self, val):
        cleaned = str(val).lower()
        if cleaned == 'na' or cleaned == 'n/a' or cleaned == '':
            return True
        else:
            return False

    def set_value(self, name, val):
        if not name == 'columns':
            self._data[name] = val

    def get_value(self, name):
        if not name == 'columns':
            if name in self._data:
                return self._data[name]

    def set_bounds(self, column_name, min, max):
        self._data['columns'][column_name] = {'min' : min, 'max' : max}

    def get_bounds(self, column_name):
        if column_name in self._data['columns']:
            return self._data['columns'][column_name]

    def check_bounds(self, column_name, val):
        if column_name in self._data["columns"]:
            col = self._data["columns"][column_name]

            col_max = None
            col_min = None

            if self._is_date(val):
                val = parse(val)
                if 'max' in col:
                    if not self._is_na(col['max']):
                        col_max = parse(col['max'])
                if 'min' in col:
                    if not self._is_na(col['min']):
                        col_min = parse(col['min'])
            else:
                if not self._is_na(col['max']):
                    col_max = col['max']
                if not self._is_na(col['min']):
                    col_min = col['min']
            if 'max' in col:
                if not self._is_na(col['max']):
                    if val > col_max:
                        return BoundsResult.MAX_ERROR
            if 'min' in col:
                if not self._is_na(col['min']):
                    if val < col_min:
                        return BoundsResult.MIN_ERROR

        return BoundsResult.VALID
    def save(self, new_filename=""):
        if not new_filename:
            new_filename = self._filename
        with open(new_filename, 'w') as f:
            json.dump(self._data, f)

