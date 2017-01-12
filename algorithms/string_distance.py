# This Python file uses the following encoding: cp1252
'''
Created on 11/11/2013

@author: mmpe

Use string matching instead
'''

from heapq import heappush, heappop
import sys


import numpy as np
from mmpe.cython_compile.cython_compile import cython_compile




class Score(object):
    def __init__(self):
        pass

    def get_score(self, a, b):
        if a == b:
            return 1
        elif a.lower() == b.lower():
            return 0.9
        else:
            return 0

class StringDistance(object):
    def __init__(self, score_function):
        self.score_function = score_function

    def get_score(self, A, B):
        scoreboard = np.zeros((len(A) + 1 , len(B) + 1))
        scoreboard[:, 0] = np.arange(len(A) + 1)
        scoreboard[0, :] = np.arange(len(B) + 1)

        for i, a in enumerate(A, 1):
            for j, b in enumerate(B, 1):
                distance = 1 - self.score_function(a, b)

                scoreboard[i, j] = min([scoreboard[i - 1, j] + 1, scoreboard[i, j - 1] + 1, scoreboard[i - 1, j - 1] + distance])

        #print ("%s[%s], %s[%s]: %.3f" % (A, a, B, b, scoreboard[i, j]))
        #print ("\n".join([str(["%.3f" % v for v in row]) for row in scoreboard]))
        #print ()

        return scoreboard[i, j]

    def score_lst_sorted(self, string, lst, thresshold=0, include_scores=False):
        score_lst = []
        for l in lst:
            score = self.get_score(string, l) / len(string)
            if score <= thresshold:
                heappush(score_lst, (score, l))
        if include_scores:
            return [(-score, string) for score, string in [heappop(score_lst) for _ in range(len(score_lst))]]
        else:
            return [string for _, string in [heappop(score_lst) for _ in range(len(score_lst))]]

    def score_dict(self, string, lst, thresshold=0):
        score_dict = {}
        for l in lst:
            score_dict[l] = self.get_score(string, l) / len(string)
        return score_dict



class SmartDistance(StringDistance):

    def __init__(self, special_scores=[]):
        self.special_scores = {}
        for a, b, score in special_scores:
            if a > b:
                a, b = b, a
            if a not in self.special_scores:
                self.special_scores[a] = {}
            self.special_scores[a][b] = score

        def score_function(a, b):
            if a == b:
                return 1
            elif a.lower() == b.lower():
                return 0.9
            try:
                if a > b:
                    a, b = b, a
                return self.special_scores[a][b]
            except KeyError:
                return .000
        StringDistance.__init__(self, score_function)



#print (SmartMatch([(u"ø", "o", 1)]).sort_lst("Ford", ["Porche", "ford", "opel", "Opel", "Fo rd", "Førd"], .3))
