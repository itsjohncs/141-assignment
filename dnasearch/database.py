def load_database(database):
    """
    Returns a generator that provides `Organism` objects pulled from the
    database.

    >>> db = load_database(StringIO.StringIO(">a\n>AGC\n>b\n>CGA\n"))
    >>> for i in db:
    ...     print i
    Organism(description = "a", sequence = "AGC")
    Organism(description = "b", sequence = "CGA")

    :param database: A file-like object that contains the database.

    :returns: A generator that returns `Organism` objects.

    """

    pass
