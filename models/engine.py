import getpass
from sqlalchemy import create_engine


###############################################################################
# "Public" functions

# To skip entering username and password, supply them to this function.
def create(user=None, passwd=None, hostname="localhost", db="aperature", verbose=False):
    if user is None:
        user = _get_name()

    if passwd is None:
        passwd = _get_passwd()

    engine_info = ["postgresql://", user, ":", passwd, "@", hostname, "/", db]
    engine = create_engine("".join(engine_info))

    if verbose:
        print("Your engine has been created: ", end = "")
        print(engine)

    return engine


###############################################################################
# "Private" functions

def _get_name():
    while True:
        try:
            user = input("Enter username: ")
            return user
        except EOFError:
            print()

###########################################################

def _get_passwd():
    while True:
        try:
            passwd = getpass.getpass("Enter password: ")
            return passwd
        except EOFError:
            print()

