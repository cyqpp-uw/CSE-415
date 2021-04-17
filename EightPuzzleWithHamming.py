from EightPuzzle import *


def h(s):
    h_distance = 0
    correct_n = 0
    for i in range(3):
        for j in range(3):
            if s[i][j] != correct_n:
                h_distance += 1
            correct_n += 1
    return h_distance