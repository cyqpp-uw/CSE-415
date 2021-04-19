"""
EightPuzzleWithManhattan.py
by Kaijun Gao
UWNetID: kg52
Student Number: 1766618

Assignment 2, Part 1, in CSE 415, Spring 2021

This files contains Manhattan distance heuristic function for Eight Puzzle Problem.
"""
from EightPuzzle import *

reference_position = {1:(0, 1), 2:(0,2), 3:(1,0), 4:(1, 1), 5:(1, 2), 6:(2, 0), 7:(2, 1), 8:(2, 2)}

def h(s):
    distance = 0
    for i in range(3):
        for j in range(3):
            if s.b[i][j] != 0:
                x, y = reference_position[s.b[i][j]]
                distance += abs(x - i) + abs(y-j)
    return distance
