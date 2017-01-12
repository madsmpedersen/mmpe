import string

import numpy as np


def score_function(a, b):  #   cdef float score_function(int a, int b):
    global special_scores
    #a, b = chr(a), chr(b)
    try:
        return special_scores[a][b]
    except KeyError:
        pass
    try:
        return special_scores[b][a]
    except KeyError:
        pass
    if a == b:
        return 1.
    elif a.lower() == b.lower():
        return 0.9
    else:
        return 0.

def get_score(A, B):  #  cdef float get_score(char* A, char* B):
    #cdef int i, j
    #cdef float score
    #cdef np.ndarray[np.float64_t,ndim=2] scoreboard
    scoreboard = np.zeros((len(A) + 1 , len(B) + 1))
    scoreboard[:, 0] = np.arange(len(A) + 1)
    scoreboard[0, :] = np.arange(len(B) + 1)

    for i, a in enumerate(A, 1):
        for j, b in enumerate(B, 1):
            distance = 1 - score_function(a, b)

            scoreboard[i, j] = min([scoreboard[i - 1, j] + 1, scoreboard[i, j - 1] + 1, scoreboard[i - 1, j - 1] + distance])

#    print ("%s[%s], %s[%s]: %.3f" % (A, a, B, b, scoreboard[i, j]))
#    print ("\n".join([str(["%.3f" % v for v in row]) for row in scoreboard]))
#    print ()

    return (max(len(A), len(B)) - scoreboard[i, j])  #/ max(len(A), len(B))


def score_dict(string, lst, _special_scores={}, thresshold=0):
    global special_scores
    score_dict = {}
    special_scores = _special_scores
    for l in lst:
        score_dict[l] = float(get_score(string, l))
    return score_dict

def generate_special_scores(special_scores):
    special_score_dict = {}
    for a, b, score in special_scores:
        if a > b:
            a, b = b, a
        if a not in special_score_dict:
            special_score_dict[a] = {}
        special_score_dict[a][b] = score
    special_score_dict[' '] = { b:.8 for b in string.ascii_letters + string.digits}
    return special_score_dict

