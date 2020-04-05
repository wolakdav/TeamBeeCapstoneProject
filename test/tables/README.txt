
test_table.py extends Table with a dummy subclass. This is done to allow the
various subclasses of Table to not need to redundantly check inherited members
and methods. Additionally, once subclasses have tested the abstract members of
Table that they implemented (and any other changed members), they can leverage
the tests from test_table.py to assert all of the inherited methods are
correct. If a subclass overrides an inherited method, they obviously need to
test it. as an extension of this, subclasses will need to test their
constructor, but, assuming they are aiming for the same functionality, they
can just copy and paste the various constructor tests.

