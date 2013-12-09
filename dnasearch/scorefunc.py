# stdlib
import ConfigParser
import re
import StringIO

DEFAULT_SCORE_INI = \
"""
[score_definition]
matrix =
    1.0 -0.1 -0.1 -0.15
    -0.1 1.0 -0.15 -0.1
    -0.1 -0.15 1.0 -0.1
    -0.15 -0.1 -0.1 1.0
gap_formula = 0.2 + 0.05 * length

"""

def make_score_functions(score_file):
    """
    Reads a score file and returns two scoring functions
    ``(sub_score, gap_score)``.

    The first function defines the cost of substitutions and has the signature
    ``sub_score(a, b)`` where ``a`` and ``b`` are two genome symbols. The
    function should be symmetric such that ``sub_score(a, b)`` is equivalent to
    ``sub_score(b, a)`` in all cases.

    The second function defines the cost of gaps, and has the signature
    ``gap_score(length)`` where ``length`` is the length of the gap.

    The score file's format should conform to the INI file syntax as expected
    by Python's standard ConfigParser module. A section titled
    ``score_definition`` will be inspected for ``matrix`` and ``gap_formula``
    values.

    ``matrix`` should be a 4x4 matrix of numbers representing the substition
    penalties. The matrix should be ordered like the following...

    ```
    - A G C T
    A 0 1 2 3
    G 1 0 4 5
    C 2 4 0 6
    T 3 5 6 0
    ```

    Note however that the headers should not be present.

    ``gap_formula`` should be a valid Python expression that yields a number
    based on the value of the variable ``length``. An example value would be
    ``length * 2`` which would mean that a gap costs twice its length.

    Here is a full example of a score file.

    ```ini
    [score_definition]
    matrix =
        0 1 2 3
        1 0 4 5
        2 4 0 6
        3 5 6 0
    gap_formula = length * 2
    ```

    :param score_file: A file-like object containing the file that defines
        scoring functions. If ``None`` a default score file will be used that
        uses the matrix and gap penalty described in the spec.

    :returns: A two-tuple ``(sub_score, gap_score)``. See above for details.

    """

    if score_file is None:
        score_file = StringIO.StringIO(DEFAULT_SCORE_INI)

    parser = ConfigParser.SafeConfigParser()
    parser.readfp(score_file)

    # Create and quickly test the gap_score function
    gap_formula = parser.get("score_definition", "gap_formula")
    gap_score = lambda length: eval(gap_formula)
    try:
        gap_score(1)
    except:
        raise RuntimeError("gap_formula not valid.")

    matrix_raw = parser.get("score_definition", "matrix")

    # The symbols available in the order they appear in the matrix
    symbols = ("A", "G", "C", "T")

    # Create a two dimensional list to store the resulting matrix
    matrix = [list([0] * len(symbols)) for i in range(len(symbols))]

    # Extract just the numbers
    NUMBER_RE = re.compile("-?[0-9]+\.?[0-9]*")
    numbers = [float(i) for i in NUMBER_RE.findall(matrix_raw)]
    if len(numbers) != len(symbols) ** 2:
        raise RuntimeError("Not enough values in matrix.")

    # Fill in the matrix
    for i, value in enumerate(numbers):
        matrix[i // len(symbols)][i % len(symbols)] = value

    sub_score = lambda a, b: matrix[symbols.index(a)][symbols.index(b)]

    return sub_score, gap_score
