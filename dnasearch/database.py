# internal
from .organism import Organism

def load_database(database):
    """
    Returns a generator that provides `Organism` objects pulled from the
    database.

    >>> db = load_database(StringIO.StringIO(">a\\nAGC\\n>b\\nCGA\\n"))
    >>> for i in db:
    ...     print i
    Organism(description = "a", sequence = "AGC")
    Organism(description = "b", sequence = "CGA")

    :param database: A file-like object that contains the database.

    :returns: A generator that returns `Organism` objects.

    """

    while True:
        description = database.readline().strip()
        sequence = database.readline().strip()

        # Check if we've hit the end of the file
        if description == "" and sequence == "":
            break

        # Ensure that the format is what we expect
        if description[0] != ">":
            raise RuntimeError("Poorly formatted database file.")

        yield Organism(description[1:], sequence)
