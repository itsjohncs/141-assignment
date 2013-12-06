from .. import similarity

#from pytest import *

if similarity.score("AACCTGACATCTT", "CCAGCGTCAACTT", 1, 1) != (7.35, 'CCTGA__CATCTT', 'CCAGCGTCAACTT'):
    print "Failed Test: 1"

if similarity.score("CCAGCGTCAACTT", "AACCTGACATCTT", 1, 1) != (7.35, 'AG__CGTCAACTT', 'AACCTGACATCTT'):
    print "Failed Test: 2"

if similarity.score("AAACCCGGGTTT", "AAACCCGGGTTT", 1, 1) != (12.00, 'AAACCCGGGTTT', 'AAACCCGGGTTT'):
    print "Failed Test: 3"

if similarity.score("ACGT", "CATG", 1, 1) != (1.9, '_ACG', 'CATG'):
    print "Failed Test: 4"

if similarity.score('A','A',1,1)!=(1,'A','A'):
    print "Failed Test: 5"

if similarity.score("CATG", "ACGT", 1, 1) != (1.9,'_CAT', 'ACGT'):
    print "Failed Test: 6"
