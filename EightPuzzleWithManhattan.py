from EightPuzzle import *

def h(s):
    m_distance = 0
    correct_n = 0
    for i in range(3):
        for j in range(3):
            if s[i][j] != correct_n:
                for k in range(3):
                    for l in range(3):
                        if s[k][l] == correct_n:
                            m_distance += abs(k - i)
                            m_distance += abs(l - j)
            correct_n += 1
    return m_distance