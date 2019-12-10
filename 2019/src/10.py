import argparse
import collections
import itertools
import math
import unittest

def partA(positions):
    return max(count_lines_of_sight(pt, positions) for pt in positions)

def partB(positions):
    pass

def count_lines_of_sight(pt, positions):
    positions = sorted(positions, key=lambda p: distance(pt, p))

    seen = set()
    for qt in positions:
        if pt == qt:
            continue
        delta = (qt[0] - pt[0], qt[1] - pt[1])
        d = direction(delta)
        seen.add(d)

    return len(seen)


def direction(pt):
    assert pt[0] or pt[1]

    if pt[0] == 0:
        x = 0
        y = 1 if pt[1] > 0 else -1
    elif pt[1] == 0:
        x = 1 if pt[0] > 0 else -1
        y = 0
    else:
        d = math.gcd(abs(pt[0]), abs(pt[1]))
        x = pt[0] // d
        y = pt[1] // d

    return (x, y)

def distance(pt_a, pt_b):
    return abs(pt_a[0] - pt_b[0]) + abs(pt_a[1] - pt_b[1])

def parse_positions(lines):
    positions = []
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == '#':
                positions.append((x, y))

    return positions

class TestProblem(unittest.TestCase):

    grid1 = \
"""
.#..#
.....
#####
....#
...##
""".strip().split('\n')

    grid2 = \
"""
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
""".strip().split('\n')

    def test_parse(self):
        lines = self.grid1
        exp = [
                (1, 0),
                (4, 0),
                (0, 2),
                (1, 2),
                (2, 2),
                (3, 2),
                (4, 2),
                (4, 3),
                (3, 4),
                (4, 4),
        ]
        got = parse_positions(lines)
        assert got == exp

    def test_direction(self):
        d = direction((2, 0))
        assert d == (1, 0)

        d = direction((-1, 0))
        assert d == (-1, 0)

        d = direction((-10, 0))
        assert d == (-1, 0)

        d = direction((-2, 3))
        assert d == (-2, 3)

        d = direction((-4, 6))
        assert d == (-2, 3)

    def test_los_count(self):
        lines = self.grid1
        positions = parse_positions(lines)
        exp = [7, 7, 6, 7, 7, 7, 5, 7, 8, 7]
        got = [count_lines_of_sight(pt, positions) for pt in positions]
        assert got == exp

    def test_partA(self):
        lines = self.grid1
        positions = parse_positions(lines)
        assert partA(positions) == 8

    def test_partA(self):
        lines = self.grid2
        positions = parse_positions(lines)
        assert partA(positions) == 33


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    with open(args.input) as fh:
        positions = parse_positions(fh)

    print(partA(positions))
    print(partB(positions))
