"""
This file provides Hamming heuristic function for EightPuzzle
"""

from EightPuzzle import *

def h(s):
    """
    Returns the # of tiles which are out of place
    """
    count = 0
    for i in range(3):
        for j in range(3):
            if s.b[i][j] != 0 and s.b[i][j] != 3 * i + j:
                count += 1
    return count
