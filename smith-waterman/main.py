# stdlib
import collections

# Create an enumeration to keep track of what we're doing
MATCH, DELETION, INSERTION = range(3)

# The score is H(i, j) (per wikipedia's description of the algorithm) along
# with one action being one of None, MATCH, DELETION, or INSERTION.
SmithCell = collections.namedtuple("SmithCell", ["score", "action"])

def _find_direction(action):
    """
    Returns a relative position (i, j) that corresponds to the direction to
    move per this action (see the wikipedia article for more info).

    """

    lookup_table = {
        None: (0, 0),
        MATCH: (-1, -1),
        DELETION: (-1, 0),
        INSERTION: (0, -1)
    }

    return lookup_table[action]

def _find_gap_length(matrix, i, j):
    """
    Determine the length of the gap starting at (i, j) in matrix.

    """

    start_action = matrix[i][j].action
    if start_action not in (DELETION, INSERTION):
        return 0

    result = 0
    while matrix[i][j].action == start_action:
        di, dj = _find_direction(matrix[i][j].action)
        i += di
        j += dj

        result += 1

    return result

def _simple_similarity_score(a, b, sub_score, gap_score):
    """
    Calculates the score between the strings a and b without any shifting.

    """

    # The length of the current gap
    gap_length = 0

    # The owner of the current gap, may be one of None, "a", or "b".
    gap_owner = None

    final_score = 0
    for i, j in zip(a, b):
        # This shouldn't be possible and our code would act weird if it is.
        assert not (i == "_" and j == "_")

        # Figure out if there's a gap in i or j right now and whose it is
        if i == "_":
            current_gap_owner = "a"
        elif j == "_":
            current_gap_owner = "b"
        else:
            current_gap_owner = None

        # If this is the end of a gap calculate the penalty
        if gap_owner is not None and gap_owner != current_gap_owner:
            final_score -= gap_score(gap_length)

        # Add the substitution if there's no gap here
        if current_gap_owner is None:
            final_score += sub_score(i, j)

            # Reset the gap variables
            gap_length = 0
            gap_owner = None
        else:
            if gap_owner == current_gap_owner:
                gap_length += 1
            else:
                gap_length = 1
                gap_owner = current_gap_owner

    return final_score

def calculate_similarity(a, b, sub_score, gap_score):
    """
    :param a: A sequence (the entirity of this sequence may not be used). This
        is the reference string.
    :param b: Another sequence (all of this sequence is used). This is the
        query string.

    """

    # Create our matrix (len(a) + 1) x (len(b) + 1).
    matrix = [[None] * (len(b) + 1) for i in xrange(len(a) + 1)]

    # Zero our left and top borders
    for i in xrange(len(a) + 1):
        matrix[i][0] = SmithCell(0, None)
    for i in xrange(len(b) + 1):
        matrix[0][i] = SmithCell(0, None)

    # As we build the matrix we're going to keep track of what the largest
    # value is
    largest_cell = None

    # Iterate through the matrix top-down left-to-right and fill in the values.
    # Make sure to skip the zeroed borders
    for i in xrange(1, len(a) + 1):
        for j in xrange(1, len(b) + 1):
            # The score if we leave things be and match up these two symbols.
            # Note that when accessing the original strings we have to be
            # careful since we added zeroed borders
            match_score = (matrix[i - 1][j - 1].score +
                sub_score(a[i - 1], b[j - 1]))

            # The score if we add a gap to b here (deletion)
            deletion_score = (matrix[i - 1][j].score -
                gap_score(1 + _find_gap_length(matrix, i - 1, j)))

            # The score if we add a gap to a here (insertion)
            insertion_score = (matrix[i][j - 1].score -
                gap_score(1 + _find_gap_length(matrix, i, j - 1)))

            max_score = max(
                (0, None),
                (match_score, MATCH),
                (deletion_score, DELETION),
                (insertion_score, INSERTION))
            matrix[i][j] = SmithCell(*max_score)

            if largest_cell is None or largest_cell[0] < matrix[i][j].score:
                largest_cell = (matrix[i][j].score, (i, j))

    # Move through the matrix backwards and determine our path (the blue
    # arrows in the wikipedia article is visualizing this step)
    path = []
    i, j = largest_cell[1]
    while matrix[i][j].action is not None:
        path.append((i, j))

        di, dj = _find_direction(matrix[i][j].action)
        i += di
        j += dj

    # Construct the alignments and final score by walking through our path
    # backwards.
    aligned_a = []
    aligned_b = []
    for i_j in reversed(path):
        # Unpack the coordinates in the path
        i, j = i_j

        # Grab the cell at (i, j) so our code below can be more succint
        cell = matrix[i][j]

        # Contruct the two alignments per wikipedia's description. Figuring
        # out which string to add a gap to after an INSERTION vs DELETION was
        # figured out through trying both. Hard to keep it all in my head.
        if cell.action == MATCH:
            aligned_a.append(a[i - 1])
            aligned_b.append(b[j - 1])
        elif cell.action == INSERTION:
            aligned_a.append("_")
            aligned_b.append(b[j - 1])
        elif cell.action == DELETION:
            aligned_a.append(a[i - 1])
            aligned_b.append("_")

    # Figure out the number of gaps on the left and right side of aligned_b
    gaps_left, gaps_right = 0, 0
    for gaps_left, symbol in enumerate(aligned_b):
        if symbol != "_":
            break
    for gaps_right, symbol in enumerate(reversed(aligned_b)):
        if symbol != "_":
            break

    # Cut off the gaps from aligned_b and truncate aligned_a as well
    end = -gaps_right if gaps_right != 0 else None
    aligned_a = aligned_a[gaps_left:end]
    aligned_b = aligned_b[gaps_left:end]

    # For simplicity, we calculate the final score here rather than
    # incrementally above which seems to be theoretically possible.
    gap_length = 0
    gap_owner = None
    final_score = 0
    for i, j in zip(aligned_a, aligned_b):
        assert not (i == "_" and j == "_")

        if i != "_" and j != "_":
            final_score += sub_score(i, j)

            gap_length = 0
            gap_owner = None
        elif i == "_" or j == "_":
            gap_in_a = i == "_"

            if gap_owner == "a":
                gap_length += 1

    aligned_a = "".join(aligned_a)
    aligned_b = "".join(aligned_b)
    score = _simple_similarity_score(aligned_a, aligned_b, sub_score,
        gap_score)

    return aligned_a, aligned_b, score

if __name__ == "__main__":
    import dnasearch.scorefunc as scorefunc
    sub_score, gap_score = scorefunc.make_score_functions(None)

    print calculate_similarity("ACACACTA", "AGCACACA", sub_score, gap_score)
    print calculate_similarity("CGAC", "AGCACAC", sub_score, gap_score)
    print calculate_similarity("AGCACAC", "CGAC", sub_score, gap_score)
    print calculate_similarity("AACCTGACATCTT", "CCAGCGTCAACTT", sub_score, gap_score)
    print calculate_similarity("AAACCCGGGTTT", "AAACCCGGGTTT", sub_score, gap_score)
    print calculate_similarity("ACGT", "CATG", sub_score, gap_score)
