import sys
import json
from enum import Enum

class BoundsResult(Enum):
    VALID = 1     #value is within range
    MAX_ERROR = 2 #value is greater than MAX
    MIN_ERROR = 3 #value is less than MIN

class Config:    
    def load(self, filename=CONFIG_FILE, debug=False):
        with open(filename) as f:
            self._data = json.load(f)
            print(self._data)

    def set_value(self, name, val):
        self._data[name] = val

    def get_value(self, val):
        if val in self._data:
            return self._data[val]

    def check_bounds(self, column_name, val):
        if column_name in self._data['columns']:
            col = self._data['columns'][column_name]

            if col['max'] != 'NA':
                if val > col['max']:
                    return BoundsResult.MAX_ERROR

            if col['min'] != 'NA':
                if val < col['min']:
                    return BoundsResult.MIN_ERROR

            return BoundsResult.VALID

if __name__ == "__main__":
     if len(sys.argv) > 1:
         if (sys.argv[1] == 'load'):
             config = Config()
             config.load()
             print('Loaded config data.')
