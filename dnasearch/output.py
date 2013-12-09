RESET = "\033[0m"
"""Control sequence to reset colors on terminal."""

def _resolve_symbol(symbol, use_colors):
    if not use_colors:
        return symbol

    mapping = {
        "X": "\033[41m",
        "|": "\033[42m",
        " ": "\033[43m"
    }

    return mapping[symbol] + " " + RESET

def write_result(name, top_sequence, bottom_sequence, score, use_colors = True,
        console_width = 72, show_alignment = True):
    """
    Writes a single result to standard output.

    :param name: The name of the organism (which should have the genome
        ``top_sequence``).
    :param top_sequence: A sequence that will be printed at the top.
    :param bottom_sequence: A sequence that will be printed at the bottom.
    :param score: A score value.
    :param use_colors: If True, colored spaces will be used instead of symbols.
    :param console_width: The width to use when printing.
    :param show_alignment: If False, the sequences won't be printed out and
        only the score will be shown.

    :returns: ``None``

    """

    # Print the header
    print "Organism:", name
    print "Similarity Score:", score

    if not show_alignment:
        return None

    # We're printing the alignment so make a blank space between the header and
    # it.
    print

    # Ensure that the sequences are the same size, add padding where necessary
    pad_sequence = lambda seq, width: seq + "_" * (width - len(seq))
    max_width = max(len(top_sequence), len(bottom_sequence))
    top_sequence = pad_sequence(top_sequence, max_width)
    bottom_sequence = pad_sequence(bottom_sequence, max_width)

    # Create the middle row of symbols (will be converted to colors later if
    # enabled).
    middle_row = [" "] * max_width
    for i, top, bottom in zip(
            xrange(max_width), top_sequence, bottom_sequence):
        if top == "_" or bottom == "_":
            middle_row[i] = " "
        elif top == bottom:
            middle_row[i] = "|"
        else:
            middle_row[i] = "X"

    top_row = list(top_sequence)
    bottom_row = list(bottom_sequence)

    # Function get set a slice of a row
    split_row = lambda x: (x[:console_width], x[console_width:])

    while top_row:
        # Take a slice out of each row
        top_slice, top_row = split_row(top_row)
        middle_slice, middle_row = split_row(middle_row)
        bottom_slice, bottom_row = split_row(bottom_row)

        print "".join(top_slice)
        print "".join(_resolve_symbol(i, use_colors) for i in middle_slice)
        print "".join(bottom_slice)

        # If there are more rows to print, print a blank line
        if top_row:
            print

# Useful for quick testing and demoing
if __name__ == "__main__":
    import sys
    # If the user passed in some command line arguments use those,
    # otherwise just use some interesting defaults.
    if len(sys.argv) > 1:
        write_result(*[eval(i) for i in sys.argv[1:]])
    else:
        write_result("Turtle", "ABCDGEXDF" * 50, "A__DEEC" * 50, 100, True)
