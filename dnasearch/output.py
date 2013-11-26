def write_result(query_organism, other_organism, score, alignment,
        pretty = False):
    """
    Writes a single result to standard output.

    :param source_organism: An ``Organism`` object describing the organism the
            user quieried about.
    :param other_organism: An ``Organism`` object that was pulled from the
            database for comparison.
    :param score: A score value.
    :param alignment: The ideal alignment determined by our algorithm. The
            format of this is not yet well-defined. Will be ``None`` if no
            alignment should be printed.
    :param pretty: If ``True``, the output should be colored and made to be as
            human-readable as possible. Otherwise, a machine-readable format
            should be used.

    :returns: ``None``

    """

    pass
