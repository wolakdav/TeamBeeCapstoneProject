import datetime

class Logger:
    def __init__(self, debug=False, logfile='log.txt'):
        self.debug = debug
        self.logfile = logfile
        self.f = open(logfile,'a+')

    def __open(self):
        self.f = open(self.logfile,'a+')

    def __close(self):
        self.f.close()

    def log(self, message, severity='INFO'):
        self.__open()
        timestamp = datetime.datetime.now()

        if severity == 'ERROR':
            self.f.write('[ERROR]  ' + str(timestamp) + '  ' + message + '\r\n')
        elif severity == 'INFO':
            self.f.write('[INFO]  ' + str(timestamp) + '  '+ message + '\r\n')
        elif severity == 'WARNING':
            self.f.write('[WARNING]  ' + str(timestamp) + '  '+ message + '\r\n')
        elif severity == 'DEBUG':
            if self.debug:
                self.f.write('[DEBUG]  ' + str(timestamp) + '  '+ message + '\r\n')

        self.__close()
    def shutdown(self):
        self.__open()
        timestamp = datetime.datetime.now()
        self.f.write('[INFO]  ' + str(timestamp) + '  '+ 'Logger shutting down.' + '\r\n')
        self.__close()
