"""
EightPuzzleWithHamming.py
by Kaijun Gao
UWNetID: kg52
Student Number: 1766618

Assignment 2, Part 1, in CSE 415, Spring 2021

This files contains hamming distance heuristic function for Eight Puzzle Problem.
"""

from EightPuzzle import *

def h(s):
    distance = 0
    for i in range(3):
        for j in range(3):
            if s.b[i][j] != 0 and s.b[i][j] != i * 3 + j:
                distance += 1
    return distance
