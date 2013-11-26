def score(query_string, other_string, sub_score, gap_score):
    """
    Compares input strings, makes alignment strings, and uses scoring functions to calculate total similarity scores for the compared string.
    Returns similarity_score, a float total of scores of all characters in the compared string

    The first function defines the cost of substitutions and has the signature
    ``sub_score(a, b)`` where ``a`` and ``b`` are two genome symbols. The
    function should be symmetric such that ``sub_score(a, b)`` is equivalent to
    ``sub_score(b, a)`` in all cases.

    The second function defines the cost of gaps, and has the signature
    ``gap_score(length)`` where ``length`` is the length of the gap.

    :param query_string, other_string : input strings to be scored

    :param sub_score, gap_score : functions used to calculate scores of individual characters

    :returns: similarity_score : the total score of all characters in the compared string

    """

    pass
