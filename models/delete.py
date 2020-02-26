
###############################################################################
# "Public" functions

# TODO: catch that invalid SQL exception and return false
def ctran_data(engine, verbose=True):
    with engine.connect() as conn:
        conn.execute("""
                DROP TABLE "ctran_data";
                """)
    return True

