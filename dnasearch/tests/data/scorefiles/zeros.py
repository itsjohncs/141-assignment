assert sub_score("A", "A") == 0
assert sub_score("A", "C") == 0
assert sub_score("C", "A") == 0
assert sub_score("C", "_") == 0

assert gap_score(1) == 0
assert gap_score(2) == 0
assert gap_score(3) == 0
