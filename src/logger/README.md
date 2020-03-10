## Usage

`from logger import Logger`

`from logger import Severity`


`log = Logger()`

`log = Logger(debug=True, filename='mylog.txt')`

`log.log('Something went wrong', Severity.ERROR)`

`log.shutdown()`
