# Database Operations

## Overview

Database operations are handled by `Table` and its various subclasses in
`src/tables`. Currently, this includes creating and deleting the schemas used
for the different tables, as well as creating and deleting the tables as well.
Some subclasses of Table, such as `CTran_Data`, will fill the table with actual
data.  
These are the subclasses of Table:  
- `CTran_Data`  
- `Flagged_Data`  
- `Duplicated_Data`  
- `Flags`  

## Methods Provided by Table

##### `__init__(user=None, passwd=None, hostname="localhost", db_name="aperature", verbose=False, engine=None)`
This requires `user`, `passwd`, `hostname`, and `db_name` to create the engine.
None of this data is kept after the engine has been created. If `user` and
`passwd` are not supplied, a prompt will require the user to enter them.
`verbose` tells the system whether or not it should have verbose outputing.
`engine` is an alternative to using `user`, `passwd`, `hostname`, and
`db_name` as it uses the supplied Engine.url member as the instance's database
engine.

##### `Engine get_engine()`
This will return a copy of the Engine object that a class uses to connect to
its corresponding database.

##### `Pandas.DataFrame get_full_table()`
This will return a Pandas DataFrame object containing the entire table the
instance represents. If an error occurs, this will return None.

##### `bool create_schema()`
This will create the schema needed for the table the instance represents.

##### `bool delete_schema()`
This will delete the schema needed for the table the instance represents, as
well as cascade the drop.

##### `bool create_table()`
This will create the table the instance represents, as well as create the
schema the table lives within. Some subclasses have overwritten this to also
fill the newly built table with data.

##### `bool create_table()`
This will delete the table the instance represents.

## Extending Table

Subclasses should initialize these abstract members in order for Table to
function correctly.  
Additionally, subclasses should not alter `self._engine` in any capacity.

##### `self._schema`
This member will contain the schema name as a string.

##### `self._table_name`
This member will contain the table name as a string.

##### `self._index_col`
This member will contain the index column string that Pandas should use while
reading in a SQL query as a DataFrame. If there is no column that should be
used in this manner, initialize this member to `False`. For more on this
member, see Panda's documentation on `Pandas.DataFrame.read_sql`.

##### `self._expected_cols`
This member will contain a set of strings of the columns in the table for
validation purposes.
