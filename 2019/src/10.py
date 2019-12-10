import argparse
import collections
import itertools
import math
import unittest

def partA(positions):
    return max(count_lines_of_sight(pt, positions) for pt in positions)

def partB(positions, victim=200):
    origin = positions[0]
    M = count_lines_of_sight(origin, positions)

    for pt in positions[1:]:
        c = count_lines_of_sight(pt, positions)
        if c > M:
            M = c
            origin = pt

    direction_to_point = collections.defaultdict(collections.deque)
    positions.sort(key=lambda pt: distance(origin, pt))
    for pt in positions:
        if pt == origin:
            continue
        v = (pt[0] - origin[0], pt[1] - origin[1])
        direction_to_point[direction(v)].append(pt)

    clock = sorted(direction_to_point.keys(), key=lambda d: angle(d))

    # repeat through clock
    # pick element from each stack, while any left
    # stop when we find element nr 200
    c = 0
    for d in itertools.cycle(clock):
        pts = direction_to_point[d]
        if not pts:
            continue

        pt = pts.popleft()
        c += 1
        if c == victim:
            return pt

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

def angle(pt):
    """
    pt is a direction.
    Compute the angle pt defines, in the range [0, 2pi],
    but rotate the angle so (0, -1) is angle 0.
    """
    x, y = pt
    assert x or y

    if x == 0:
        if y < 0:
            return 0
        else:
            return math.pi

    clock = 1 * math.atan(y / x) + math.pi / 2
    if x < 0:
        clock += math.pi

    return clock


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

    grid3 = \
"""
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
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

    def test_partB_1(self):
        lines = self.grid3
        positions = parse_positions(lines)
        assert partB(positions, 1) == (11, 12)

    def test_partB_2(self):
        lines = self.grid3
        positions = parse_positions(lines)
        assert partB(positions, 2) == (12, 1)

    def test_partB(self):
        lines = self.grid3
        positions = parse_positions(lines)
        assert partB(positions) == (8, 2)

    def test_angle_1(self):
        assert angle((0, -1)) == 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    with open(args.input) as fh:
        positions = parse_positions(fh)

    print(partA(positions))
    pt = partB(positions)
    print(pt[0] * 100 + pt[1])
