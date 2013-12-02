# stdlib
import ConfigParser
import re

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

    ``matrix`` should be a 5x5 matrix of numbers representing the substition
    penalties. The matrix should be ordered like the following...

    ```
      A G C T _
    A 0 1 2 3 4
    G 1 0 5 6 7
    C 2 5 0 8 9
    T 3 6 8 0 1
    _ 4 7 9 1 0
    ```

    Note however that the headers should not be present.

    ``gap_formula`` should be a valid Python expression that yields a number
    based on the value of the variable ``length``. An example value would be
    ``length * 2`` which would mean that a gap costs twice its length.

    Here is a full example of a score file.

    ```ini
    [score_definition]
    matrix =
        0 1 2 3 4
        1 0 5 6 7
        2 5 0 8 9
        3 6 8 0 1
        4 7 9 1 0
    gap_formula = length * 2
    ```

    :param score_file: A file-like object containing the file that defines
            scoring functions.

    :returns: A two-tuple ``(sub_score, gap_score)``. See above for details.

    """

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
    symbols = ("A", "G", "C", "T", "_")

    # Create a two dimensional list to store the resulting matrix
    matrix = [list([0] * len(symbols)) for i in range(len(symbols))]

    # Extract just the numbers
    NUMBER_RE = re.compile("[0-9]+\.?[0-9]*")
    numbers = [float(i) for i in NUMBER_RE.findall(matrix_raw)]
    if len(numbers) != len(symbols) ** 2:
        raise RuntimeError("Not enough values in matrix.")

    # Fill in the matrix
    for i, value in enumerate(numbers):
        matrix[i // len(symbols)][i % len(symbols)] = value

    sub_score = lambda a, b: matrix[symbols.index(a)][symbols.index(b)]

    return sub_score, gap_score
