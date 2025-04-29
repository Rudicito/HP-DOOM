from math import *

def dist(p1, p2):
    """
    Calculates the distance between two points in a 2D plane.

    p1, p2: tuples or lists representing coordinates (x, y)
    """
    x1, y1 = p1
    x2, y2 = p2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def isclose(a, b, rel_tol=1e-9, abs_tol=0.0):
    """
    Checks if two numbers are close to each other.

    a, b: The numbers to compare.
    rel_tol: Relative tolerance (default is 1e-9).
    abs_tol: Absolute tolerance (default is 0.0).
    """
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)
