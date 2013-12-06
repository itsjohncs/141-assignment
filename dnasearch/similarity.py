def score(reference, query_str, sub_score, gap_score):
    ref = reference.strip()
    query = query_str.strip()

    m = len(ref)
    n = len(query)

    score = [[0]*(n+1) for i in xrange(m+1)]
    bt = [[0]*(n+1) for i in xrange(m+1)]
    gaps = [[0]*(n+1) for i in xrange(m+1)]
    score[0][0] = 0
    bt[0][0] = -1

    DELETION, INSERTION, MATCH = range(3)

    for i in range(1,m+1):
        bt[i][0] = DELETION
        score[i][0] = -.2

    gaps[0][1] = 1
    for i in range(2,n+1):
        gaps[0][i] = 1 + gaps[0][i-1]
    gap_len = 0
    for i in range(1,m+1):
        for j in range(1,n+1):
            if j > 1:
                gap_len = gaps[i-1][j]
            deletion = (score[i - 1][j] - gap_score(gap_len+1), DELETION)
            gap_len = 0
            if i > 1:
                gap_len = gaps[i][j-1]
            insertion = (score[i][j - 1] - gap_score(gap_len+1), INSERTION)
            match = (score[i-1][j-1]+ sub_score(ref[i-1],query[j-1]), MATCH)
            score[i][j], bt[i][j] = max(deletion, insertion, match)
            if bt[i][j] == DELETION:
                gaps[i][j] = gaps[i-1][j] + 1
            elif bt[i][j] == INSERTION:
                gaps[i][j] = gaps[i][j-1] + 1
            else:
                gaps[i][j] = 0
    similarity_i = round(score[m][n-1],2)
    similarity_d = round(score[m-1][n],2)
    similarity_m = round(score[m][n],2)
    if similarity_d > similarity_m:
        if similarity_i > similarity_d:
            bt1 = [[0]*(n) for i in xrange(m+1)]
            for i in range(1,m+1):
                for j in range(1,n):
                    bt1[i][j] = bt[i][j]
            bt = bt1
            similarity = similarity_i
        else:
            bt1 = [[0]*(n+1) for i in xrange(m)]
            for i in range(1,m):
                for j in range(1,n+1):
                    bt1[i][j] = bt[i][j]
            bt = bt1
            similarity = similarity_d
            ref = ref[:m-1]
    elif similarity_i > similarity_m:
        bt1 = [[0]*(n) for i in xrange(m+1)]
        for i in range(1,m+1):
            for j in range(1,n):
                bt1[i][j] = bt[i][j]
        bt = bt1
        similarity = similarity_i
    else:
        similarity = similarity_m

    #print('\n'.join([''.join(['{:6}'.format(round(item,2)) for item in row]) for row in score]))
    #print('\n'.join([''.join(['{:6}'.format(item) for item in row]) for row in bt]))
    #print('\n'.join([''.join(['{:6}'.format(item) for item in row]) for row in gaps]))
    #print ref, query

    a,b = backtrace(ref,query,bt)

    return similarity, a, b

def backtrace(ref,query,bt):
    if len(ref) == 1 and len(query) == 1:
        return ref,query

    i = len(ref)-1
    j = len(query)-1
    a = b = ""

    DELETION, INSERTION, MATCH = range(3)

    while i >= 0 or j >= 0:
        if i < 0 or j < 0:
            break
        if bt[i][j] == MATCH:
            if len(a) >= 1 and a[len(a)-1] == '_':
                a += ref[i+1]
            if len(b) >= 1 and b[len(b)-1] == '_':
                b += query[j+1]
            a += ref[i]
            b += query[j]
            i -= 1
            j -= 1
        elif bt[i][j] == INSERTION:
            if len(b) > 0 and b[len(b)-1] != '_' or len(b) == 0:
                b += query[j]
            b += '_'
            j -= 1
        elif bt[i][j] == DELETION:
            if len(a) > 0 and a[len(a)-1] != '_' or len(a) == 0:
                a += ref[i]
            a += '_'
            i -= 1
        else:
            if query[j] == ref[i]:
                a += ref[0]
                b += ref[0]
            break

    if j > 1: k = j+1
    elif j == 1: k = 1+1
    else: k = 0
    a = a[::-1]

    for j in reversed(xrange(0,k)):
        b += query[j]
        if len(b) < len(a):
            a = a[1:]

    while len(a) < len(b):
        a = '_' + a
    while len(a) > len(b):
        a = a[:len(a)-2]
    return a,b[::-1]

#~ def sub(a,b):
    #~ mat = [[0]*4 for i in range(4)]
    #~ for i in range(4): mat[i][i] = 1.0
    #~ mat[0][1] = mat[1][0] = -0.1
    #~ mat[0][2] = mat[2][0] = -0.1
    #~ mat[0][3] = mat[3][0] = -0.15
    #~ mat[1][2] = mat[2][1] = -0.15
    #~ mat[1][3] = mat[3][1] = -0.1
    #~ mat[2][3] = mat[3][2] = -0.1
#~
    #~ str = "AGCT"
    #~ for i in range(0,4):
        #~ if (str[i] == a):
            #~ ret = i
            #~
    #~ str = "AGCT"
    #~ for i in range(0,4):
        #~ if (str[i] == b):
            #~ ret2 = i
            #~
    #~ return mat[ret][ret2]
     #~
#~ def gap(gap_len):
    #~ if gap_len == 1:
        #~ return .2
    #~ return .05

