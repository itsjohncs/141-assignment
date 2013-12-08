# internal
from .. import scorefunc
from .. import similarity

# external
import pytest

TEST_CASES = [
    (
        ("AACCTGACATCTT", "CCAGCGTCAACTT"),
        (7.35, "CCTGA__CATCTT", "CCAGCGTCAACTT")
    ),
    (
        ("CCAGCGTCAACTT", "AACCTGACATCTT"),
        (7.35, "AG__CGTCAACTT", "AACCTGACATCTT")
    ),
    (
        ("AAACCCGGGTTT", "AAACCCGGGTTT"),
        (12.00, "AAACCCGGGTTT", "AAACCCGGGTTT")
    ),
    (
        ("ACGT", "CATG"),
        (1.9, "_ACG", "CATG")
    ),
    (
        ("A","A"),
        (1, "A", "A")
    ),
    (
        ("CATG", "ACGT"),
        (1.9, "_CAT", "ACGT")
    )
]

@pytest.mark.parametrize("test_case", TEST_CASES)
def test_similarity(test_case):
    arguments, expected_result = test_case

    # Use the default substition and gap scores
    sub_score, gap_score = scorefunc.make_score_functions(None)

    actual_result = similarity.score(
        *arguments, sub_score = sub_score, gap_score = gap_score)
    assert actual_result == expected_result
