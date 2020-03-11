import datetime
import os
from enum import Enum

class Severity(Enum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4

class Logger:    
    def start(self, filename='log.txt', debug=False):
        self.debug = debug
        self._f = open(filename,'a+')

        if self.debug:
            self._f.write('[DEBUG]  {}  {} \n'.format( str(datetime.datetime.now()), 'Logger started.'))

    def log(self, message, severity = Severity.INFO):
        timestamp = datetime.datetime.now()

        if severity == Severity.ERROR:
            self._f.write('[ERROR]  {}  {} \n'.format(timestamp, message))
        elif severity == Severity.INFO:
            self._f.write('[INFO]  {}  {} \n'.format(timestamp, message))
        elif severity == Severity.WARNING:
            self._f.write('[WARNING]  {}  {} \n'.format(timestamp, message))
        elif severity == Severity.DEBUG:
            if self.debug:
                self._f.write('[DEBUG]  {}  {} \n'.format(timestamp, message))
                
        self._f.flush()
        os.fsync(self._f)

    def stop(self):
        if self.debug:
            self._f.write('[DEBUG]  {}  {} \n'.format( str(datetime.datetime.now()), 'Logger shutting down.'))
        self._f.close()
