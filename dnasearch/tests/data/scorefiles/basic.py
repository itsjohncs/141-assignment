assert sub_score("A", "A") == 0
assert sub_score("A", "C") == 2
assert sub_score("C", "A") == 2
assert sub_score("C", "_") == 9

assert gap_score(1) == 2
assert gap_score(2) == 4
assert gap_score(3) == 6
