import argparse
import collections
import datetime
import itertools
import math
import re
import unittest

def partA(moons):
    for _ in range(1000):
        moons = step(moons)

    return energy(moons)

def partB(moons):
    positions = { frozenset(x for x in moons) }
    i = 0
    while True:
        moons = step(moons)
        i += 1

        if i % 100000 == 0:
            print(datetime.datetime.now())

        pos = frozenset(x for x in moons)
        if pos in positions:
            return i
        
        positions.add(pos)

def step(moons):
    new = []
    gs = {x: Vector.zero(len(x)) for x, _ in moons}

    for (x, vx), (y, vy) in itertools.combinations(moons, 2):
        g = gravity(x, y)
        gs[x] = gs[x] + g
        gs[y] = gs[y] - g

    for x, vx in moons:
        nvx = vx + gs[x]
        new.append((x + nvx, nvx))

    return new

class Vector:

    def __init__(self, *coords):
        self.coords = tuple(coords)

    def __add__(self, other):
        assert len(self.coords) == len(other.coords)
        cs = [x + y for x, y in zip(self.coords, other.coords)]
        return Vector(*cs)

    def __sub__(self, other):
        assert len(self.coords) == len(other.coords)
        cs = [x - y for x, y in zip(self.coords, other.coords)]
        return Vector(*cs)

    def __neg__(self):
        cs = [-1 * x for x in self.coords]
        return Vector(*cs)

    def __eq__(self, other):
        assert len(self.coords) == len(other.coords)
        return self.coords == other.coords

    def __hash__(self):
        return self.coords.__hash__()

    def __repr__(self):
        return self.coords.__repr__()

    def __str__(self):
        return self.coords.__str__()

    def __len__(self):
        return len(self.coords)

    def __iter__(self):
        return self.coords.__iter__()

    def __abs__(self):
        return sum(abs(x) for x in self.coords)

    @staticmethod
    def zero(n):
        assert n >= 0
        zs = [0] * n
        return Vector(*zs)

def energy(moons):
    return sum(abs(x) * abs(vx) for x, vx in moons)

def gravity(xs, ys):
    # Note: gravity is antisymmetric.
    # Computes the vector that applies to xs (- this applies to ys)
    cs = []
    for x, y in zip(xs, ys):
        if x < y:
            cs.append(1)
        elif x == y:
            cs.append(0)
        else:
            cs.append(-1)
    return Vector(*cs)


def parse_moons(lines):
    positions = []
    for line in lines:
        m = re.search(r'x=(-?[0-9]+), y=(-?[0-9]+), z=(-?[0-9]+)', line)
        assert m is not None
        positions.append(Vector(int(m.group(1)), int(m.group(2)), int(m.group(3))))

    return [(x, Vector.zero(len(x))) for x in positions]


class TestProblem(unittest.TestCase):

    def test_1(self):
        lines = """
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
""".strip().split('\n')
        moons = parse_moons(lines)

        step0 = [
            (Vector(-1, 0, 2), Vector(0, 0, 0)),
            (Vector(2, -10, -7), Vector(0, 0, 0)),
            (Vector(4, -8, 8), Vector(0, 0, 0)),
            (Vector(3, 5, -1), Vector(0, 0, 0)),
        ]
        assert moons == step0

        step1 = [
            (Vector(2, -1, 1), Vector(3, -1, -1)),
            (Vector(3, -7, -4), Vector(1, 3, 3)),
            (Vector(1, -7, 5), Vector(-3, 1, -3)),
            (Vector(2, 2, 0), Vector(-1, -3, 1)),
        ]
        moons = step(moons)
        assert len(moons) == len(step1)
        assert set(moons) == set(step1)

        step2 = [
            (Vector(5, -3, -1), Vector(3, -2, -2)),
            (Vector(1, -2, 2), Vector(-2, 5, 6)),
            (Vector(1, -4, -1), Vector(0, 3, -6)),
            (Vector(1, -4, 2), Vector(-1, -6, 2)),
        ]
        moons = step(moons)
        assert len(moons) == len(step2)
        assert set(moons) == set(step2)

    def test_2(self):
        lines = """
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
""".strip().split('\n')
        moons = parse_moons(lines)

        for _ in range(10):
            moons = step(moons)

        assert energy(moons) == 179

    def test_3(self):
        lines = """
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
""".strip().split('\n')
        moons = parse_moons(lines)

        assert partB(moons) == 2772

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    with open(args.input) as fh:
        moons = parse_moons(fh)

    print(partA(moons))
    print(partB(moons))
