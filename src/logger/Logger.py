import datetime
import os
from enum import Enum

class Severity(Enum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4

class Logger:
    
    def __init__(self, debug=False, filename='log.txt'):
        self.debug = debug
        self.filename = filename
        self._f = open(self.filename,'a+')

        self._f.write('[{}]  {}  {} \n'.format( 'INFO', str(datetime.datetime.now()), 'Logger started.'))


    def log(self, message, severity=Severity.INFO):
        timestamp = datetime.datetime.now()

        if severity == Severity.ERROR:
            self._f.write('[{}]  {}  {} \n'.format('ERROR', str(timestamp), message))
        elif severity == Severity.INFO:
            self._f.write('[{}]  {}  {} \n'.format('INFO', str(timestamp), message))
        elif severity == Severity.WARNING:
            self._f.write('[{}]  {}  {} \n'.format('WARNING', str(timestamp), message))
        elif severity == Severity.DEBUG:
            if self.debug:
                self._f.write('[{}]  {}  {} \n'.format('DEBUG', str(timestamp), message))
                
        self._f.flush()
        os.fsync(self._f)

    def shutdown(self):
        self._f.write('[{}]  {}  {} \n'.format('INFO', str(datetime.datetime.now()), 'Logger shutting down.'))
        self._f.close()
