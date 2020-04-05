
test_table.py extends Table with a dummy subclass. This is done to allow the
various subclasses of Table to not need to redundantly check inherited members
and methods. Additionally, once subclasses have tested the abstract members of
Table that they implemented (and any other changed members), they can leverage
the tests from test_table.py to assert all of the inherited methods are
correct. If a subclass overrides an inherited method, they obviously need to
test it.

