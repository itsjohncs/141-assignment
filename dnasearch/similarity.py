"""
Compares input strings, makes alignment strings,
and uses scoring functions to calculate total similarity
scores for the compared string. Returns similarity_score,
a float total of scores of all characters in the compared string
"""
def score(query_str, other_str, sub_score, gap_score):
    query_str = x = query_str.strip()
    other_str = y = other_str.strip()
    q = len(query_str)
    o = len(other_str)

    ins = -0.2 #same as delete cost
    scores = [[0]*(o+1) for i in xrange(q+1)]
    scores[0][0] = 0

    #default substitution score matrix
    mat = [[0]*4 for i in range(4)]
    for i in range(4): mat[i][i] = 1.0
    mat[0][1] = mat[1][0] = -0.1
    mat[0][2] = mat[2][0] = -0.1
    mat[0][3] = mat[3][0] = -0.15
    mat[1][2] = mat[2][1] = -0.15
    mat[1][3] = mat[3][1] = -0.1
    mat[2][3] = mat[3][2] = -0.1

    #initiate score matrix worst-case scores
    for i in range(1,q):
        scores[i][0]= scores[i-1][0]+ins

    for j in range(1,o):
        scores[0][j]= scores[0][j-1]+ins

    DELETION, INSERTION, MATCH = range(3)
    #print "d", DELETION
    #print "i", INSERTION
    #print "m", MATCH

    bt = [[0]*(o+1) for i in xrange(q+1)]

    #fills score and backtrace matrices with values and paths respectively
    for i in range(1,q):
        for j in range(1,o):
            deletion = (scores[i-1][j] -0.2, DELETION)
            insertion = (scores[i][j-1] -0.2, INSERTION)
            match = (scores[i-1][j-1]+mat[def_sub(query_str[i])][def_sub(other_str[j])], MATCH)
            scores[i][j], bt[i][j] = max((0, 0), deletion, insertion, match)

    coord = q-1,o-1
    q = int(q)
    o = int(o)
    similarity = round(scores[q-1][o-1],2)

    #prints score and backtrace matrices, and similarity score before
    #gaps are considered

    #print('\n'.join([''.join(['{:6}'.format(round(item,2)) for item in row]) for row in scores]))
    #print "before gap length changes score: ",similarity
    #print('\n'.join([''.join(['{:6}'.format(item) for item in row]) for row in bt]))

    similarity,a,b = backtrace(similarity,query_str,other_str,bt,DELETION,INSERTION,MATCH)
    #print "After gap length changes score: ",similarity
    #print a
    #print b

    return similarity, a, b

"""
default substitution method, using table from assignment specs,
labeled mat in previous function
"""
def def_sub(ch):
    str = "AGCT"
    for i in range(0,4):
        if (str[i] == ch):
            return i
    print "Unknown Character Found, Incorrect Results Imminent."
    return -1
"""
backtrace method, uses default gap scoring as defined in assignment
specifications, and sets alignment strings according to the backtrace
matrix
"""
def backtrace(score,query_str,other_str,bt,DELETION,INSERTION,MATCH):
    i = len(query_str)-1
    j = len(other_str)-1
    a = b = ''
    gap_size = 0
    while i>0 or j>0:
        if i < 0 or j < 0:
            break
        if bt[i][j] == MATCH:
            if gap_size > 0:
                score = score - def_gap(gap_size)
            gap_size = 0
            i -= 1
            j -= 1
            a = a+ query_str[i+1]
            b = b+ other_str[j+1]
        elif bt[i][j] == INSERTION:
            ++gap_size
            j -= 1
            a = a+'_'
            b = b+other_str[j+1]
        elif bt[i][j] == DELETION:
            ++gap_size
            i -= 1
            a = a+query_str[i+1]
            b = b+'_'

    return score,a[::-1],b[::-1]

def def_gap(gap_size):
    if gap_size > 1:
        return (gap_size-1)*.05
    return 0
