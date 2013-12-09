# internal
from .. import similarity

# external
import pytest

TEST_CASES = [
    (
        ("AACCTGACATCTT", "CCAGCGTCAACTT"),
        (7.35, "CC__TGACATCTT", "CCAGCGTCAACTT")
    ),
    (
        ("CCAGCGTCAACTT", "AACCTGACATCTT"),
        (7.35, "CCAGCGTCAACTT", "CC__TGACATCTT")
    ),
    (
        ("AAACCCGGGTTT", "AAACCCGGGTTT"),
        (12.00, "AAACCCGGGTTT", "AAACCCGGGTTT")
    ),
    (
        ("ACGT", "CATG"),
        (1.9, "ACG", "ATG")
    ),
    (
        ("A","A"),
        (1, "A", "A")
    ),
    (
        ("CATG", "ACGT"),
        (1.9, "CAT", "CGT")
    )
]

@pytest.mark.parametrize("test_case", TEST_CASES)
def test_similarity(test_case):
    arguments, expected_result = test_case

    actual_result = similarity.score(*arguments)

    print actual_result[1]
    print actual_result[2]

    assert actual_result == expected_result
