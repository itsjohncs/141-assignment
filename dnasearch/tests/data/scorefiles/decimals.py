assert sub_score("A", "A") == 0
assert sub_score("A", "C") == 2.2
assert sub_score("C", "A") == 2.2
assert sub_score("C", "G") == 4.4

# Because floating point division is imprecise...
assert abs(gap_score(1) - 2.2) < 0.00001
assert abs(gap_score(2) - 4.4) < 0.00001
assert abs(gap_score(3) - 6.6) < 0.00001
