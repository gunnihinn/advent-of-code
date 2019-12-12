import argparse
import collections
import datetime
import itertools
import math
import re
import unittest

combinations = (
    (0, 1),
    (0, 2),
    (0, 3),
    (1, 2),
    (1, 3),
    (2, 3),
)

def lcm(x, y, z):
    fx = prime_factors(x)
    fy = prime_factors(y)
    fz = prime_factors(z)

    factors = set(fx.keys()) | set(fy.keys()) | set(fz.keys())
    m = 1
    for f in factors:
        a = f ** max(fx[f], fy[f], fz[f])
        m *= a

    return m


def prime_factors(n):
    factors = collections.Counter()
    i = 2
    while i <= n:
        if n % i == 0:
            factors[i] += 1
            n = n // i
        else:
            if i == 2:
                i = 3
            else:
                i += 2

    return factors

def partA(xs, ys, zs):
    for _ in range(1000):
        xs = step(xs)
        ys = step(ys)
        zs = step(zs)

    return energy(xs, ys, zs)

def partB(xs, ys, zs):
    rx = repeat(xs)
    ry = repeat(ys)
    rz = repeat(zs)

    return lcm(rx, ry, rz)


def repeat(moons):
    ps = {tuple(moons)}
    i = 0
    while True:
        moons = step(moons)
        i += 1
        m = tuple(moons)
        if m in ps:
            return i
        else:
            ps.add(m)


def step(moons):
    gs = [0, 0, 0, 0]
    for i, j in combinations:
        g = gravity(moons[2*i], moons[2*j])
        gs[i] += g
        gs[j] -= g

    new = [0] * 8
    for i in range(4):
        v = moons[2*i + 1] + gs[i]
        new[2*i] = moons[2*i] + v
        new[2*i + 1] = v

    return new

def energy(xs, ys, zs):
    e = 0
    for i in range(4):
        a = abs(xs[2*i]) + abs(ys[2*i]) + abs(zs[2*i])
        b = abs(xs[2*i+1]) + abs(ys[2*i+1]) + abs(zs[2*i+1])
        e += a * b

    return e

def gravity(x, y):
    if x < y:
        return 1
    elif x == y:
        return 0
    else:
        return -1


def parse_moons(lines):
    xs = []
    ys = []
    zs = []

    for line in lines:
        m = re.search(r'x=(-?[0-9]+), y=(-?[0-9]+), z=(-?[0-9]+)', line)
        assert m is not None
        xs.append(int(m.group(1)))
        xs.append(0)

        ys.append(int(m.group(2)))
        ys.append(0)

        zs.append(int(m.group(3)))
        zs.append(0)

    return xs, ys, zs

class TestProblem(unittest.TestCase):

    def test_1(self):
        lines = """
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
""".strip().split('\n')
        xs, ys, zs = parse_moons(lines)

        step0 = [
            [-1, 0, 2, 0, 4, 0, 3, 0],
            [0, 0, -10, 0, -8, 0, 5, 0],
            [2, 0, -7, 0, 8, 0, -1, 0],
        ]
        assert xs == step0[0]
        assert ys == step0[1]
        assert zs == step0[2]

        step1 = [
            [2, 3, 3, 1, 1, -3, 2, -1],
            [-1, -1, -7, 3, -7, 1, 2, -3],
            [1, -1, -4, 3, 5, -3, 0, 1],
        ]
        xs = step(xs)
        ys = step(ys)
        zs = step(zs)
        assert xs == step1[0]
        assert ys == step1[1]
        assert zs == step1[2]

        step2 = [
            [5, 3, 1, -2, 1, 0, 1, -1],
            [-3, -2, -2, 5, -4, 3, -4, -6],
            [-1, -2, 2, 6, -1, -6, 2, 2],
        ]
        xs = step(xs)
        ys = step(ys)
        zs = step(zs)
        assert xs == step2[0]
        assert ys == step2[1]
        assert zs == step2[2]

    def test_2(self):
        lines = """
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
""".strip().split('\n')
        xs, ys, zs = parse_moons(lines)

        for _ in range(10):
            xs = step(xs)
            ys = step(ys)
            zs = step(zs)

        assert energy(xs, ys, zs) == 179

    def test_3(self):
        lines = """
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
""".strip().split('\n')
        xs, ys, zs = parse_moons(lines)

        assert partB(xs, ys, zs) == 2772

    def test_4(self):
        exp = collections.Counter()
        exp[2] = 4
        assert prime_factors(16) == exp

        exp = collections.Counter()
        exp[2] = 2
        exp[7] = 1
        assert prime_factors(28) == exp

    def test_5(self):
        assert lcm(18, 28, 44) == 2772

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    with open(args.input) as fh:
        xs, ys, zs = parse_moons(fh)

    print(partA(xs, ys, zs))
    print(partB(xs, ys, zs))
