
TODO Complete when flag command gets refactored.

<p>main.py --date-start=YYYY-MM-DD --date-end=YYYY-MM-DD</p>
<p>main.py --select --flag=10 --limit=50</p>
<p>main.py --select --row=57 --year=2019 --service_period=1</p>

###Querying the Database

####From ctran_data.py

##### `DataFrame query_date_range`

This queries the database for all rows in the range of the start and end
date arguments. This is purpose-built for the pickup of new data based on
the automated daily run specification, in which case start and end date
will be the same date. Note that this will collect all data within the
_service dates_ associated with the start and end dates, which are
_calendar dates_. For example, if *2019-01-01* is supplied as the start
and end date, data from the previous service date that took place in the
current calendar date will **not** be collected, while data belonging to
the current service date that took place in the following calendar date
will be collected.

####From flagged_data.py

##### `DataFrame query_flags_by_row_id`


##### `DataFrame query_flags_by_flag_id`

This queries the database for the most recent instances of rows that
received the specified flag. This query has an optional _limit_ parameter
that defines the maximum number of rows to be returned, with a default
value of 100 if the argument is not supplied. Data returned includes a
maximum of _limit_ row_ids.