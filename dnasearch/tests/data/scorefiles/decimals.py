assert sub_score("A", "A") == 0
assert sub_score("A", "C") == 2.2
assert sub_score("C", "A") == 2.2
assert sub_score("C", "_") == 9.9

# Floating point multiplication is imprecise
assert abs(gap_score(1) - 2.2) < 0.0001
assert abs(gap_score(2) - 4.4) < 0.0001
assert abs(gap_score(3) - 6.6) < 0.0001
