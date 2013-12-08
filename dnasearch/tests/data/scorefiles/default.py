assert sub_score("A", "A") == 1.0
assert sub_score("A", "C") == -0.1
assert sub_score("C", "A") == -0.1
assert sub_score("C", "G") == -0.15

# Because floating point division is imprecise...
assert abs(gap_score(1) - 0.2) < 0.00001
assert abs(gap_score(2) - 0.05) < 0.00001
assert abs(gap_score(3) - 0.05) < 0.00001
