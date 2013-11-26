def make_score_function(score_file):
    """
    Reads a score file and returns two scoring functions
    ``(sub_score, gap_score)``.

    The first function defines the cost of substitutions and has the signature
    ``sub_score(a, b)`` where ``a`` and ``b`` are two genome symbols. The
    function should be symmetric such that ``sub_score(a, b)`` is equivalent to
    ``sub_score(b, a)`` in all cases.

    The second function defines the cost of gaps, and has the signature
    ``gap_score(length)`` where ``length`` is the length of the gap.

    :param score_file: A file-like object containing the file that defines
            scoring functions.

    :returns: A two-tuple ``(sub_score, gap_score)``. See above for details.

    """

    pass
