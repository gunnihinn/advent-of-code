import argparse
import collections
import unittest


def partA(wires):
    grid = collections.defaultdict(set)

    x, y = (0, 0)
    wire = wires[0]
    for d, l in wire:
        if d == "U":
            for w in range(l + 1):
                grid[(x, y + w)].add(1)
            y += l
        elif d == "D":
            for w in range(l + 1):
                grid[(x, y - w)].add(1)
            y -= l
        elif d == "L":
            for z in range(l + 1):
                grid[(x - z, y)].add(1)
            x -= l
        elif d == "R":
            for z in range(l + 1):
                grid[(x + z, y)].add(1)
            x += l
        else:
            raise ValueError("Unknown direction '{}'".format(d))

    wire = wires[1]
    x, y = (0, 0)
    for d, l in wire:
        if d == "U":
            for w in range(l + 1):
                grid[(x, y + w)].add(2)
            y += l
        elif d == "D":
            for w in range(l + 1):
                grid[(x, y - w)].add(2)
            y -= l
        elif d == "L":
            for z in range(l + 1):
                grid[(x - z, y)].add(2)
            x -= l
        elif d == "R":
            for z in range(l + 1):
                grid[(x + z, y)].add(2)
            x += l
        else:
            raise ValueError("Unknown direction '{}'".format(d))

    grid.pop((0, 0))
    crossings = {k for k, v in grid.items() if len(v) == 2}
    return min(abs(x) + abs(y) for x, y in crossings)


def partB(wires):
    grid1 = collections.defaultdict(dict)

    x, y = (0, 0)
    wire = wires[0]
    steps = 0
    for d, l in wire:
        if d == "U":
            for w in range(1, l + 1):
                steps += 1
                p = (x, y+w)
                if p not in grid1:
                    grid1[p] = steps
            y += l
        elif d == "D":
            for w in range(1, l + 1):
                steps += 1
                p = (x, y-w)
                if p not in grid1:
                    grid1[p] = steps
            y -= l
        elif d == "L":
            for z in range(1, l + 1):
                steps += 1
                p = (x-z, y)
                if p not in grid1:
                    grid1[p] = steps
            x -= l
        elif d == "R":
            for z in range(1, l + 1):
                steps += 1
                p = (x+z, y)
                if p not in grid1:
                    grid1[p] = steps
            x += l
        else:
            raise ValueError("Unknown direction '{}'".format(d))

    grid2 = collections.defaultdict(dict)
    wire = wires[1]
    x, y = (0, 0)
    steps = 0
    for d, l in wire:
        if d == "U":
            for w in range(1, l + 1):
                steps += 1
                p = (x, y+w)
                if p not in grid2:
                    grid2[p] = steps
            y += l
        elif d == "D":
            for w in range(1, l + 1):
                steps += 1
                p = (x, y-w)
                if p not in grid2:
                    grid2[p] = steps
            y -= l
        elif d == "L":
            for z in range(1, l + 1):
                steps += 1
                p = (x-z, y)
                if p not in grid2:
                    grid2[p] = steps
            x -= l
        elif d == "R":
            for z in range(1, l + 1):
                steps += 1
                p = (x+z, y)
                if p not in grid2:
                    grid2[p] = steps
            x += l
        else:
            raise ValueError("Unknown direction '{}'".format(d))

    if (0, 0) in grid1:
        grid1.pop((0, 0))
    if (0, 0) in grid2:
        grid2.pop((0, 0))
    crossings = grid1.keys() & grid2.keys()
    return min(grid1[k] + grid2[k] for k in crossings)


class TestProblem(unittest.TestCase):
    def test_run0(self):
        wires = [
            [("R", 8), ("U", 5), ("L", 5), ("D", 3)],
            [("U", 7), ("R", 6), ("D", 4), ("L", 4)],
        ]
        self.assertEqual(partA(wires), 6)

    def test_run1(self):
        wires = [
            [
                ("R", 75),
                ("D", 30),
                ("R", 83),
                ("U", 83),
                ("L", 12),
                ("D", 49),
                ("R", 71),
                ("U", 7),
                ("L", 72),
            ],
            [
                ("U", 62),
                ("R", 66),
                ("U", 55),
                ("R", 34),
                ("D", 71),
                ("R", 55),
                ("D", 58),
                ("R", 83),
            ],
        ]
        self.assertEqual(partA(wires), 159)

    def test_run2(self):
        wires = [
            [
                ("R", 98),
                ("U", 47),
                ("R", 26),
                ("D", 63),
                ("R", 33),
                ("U", 87),
                ("L", 62),
                ("D", 20),
                ("R", 33),
                ("U", 53),
                ("R", 51),
            ],
            [
                ("U", 98),
                ("R", 91),
                ("D", 20),
                ("R", 16),
                ("D", 67),
                ("R", 40),
                ("U", 7),
                ("R", 15),
                ("U", 6),
                ("R", 7),
            ],
        ]
        self.assertEqual(partA(wires), 135)

    def test_run0b(self):
        wires = [
            [("R", 8), ("U", 5), ("L", 5), ("D", 3)],
            [("U", 7), ("R", 6), ("D", 4), ("L", 4)],
        ]
        import pdb; pdb.set_trace()
        self.assertEqual(partB(wires), 30)

    def test_run1b(self):
        wires = [
            [
                ("R", 75),
                ("D", 30),
                ("R", 83),
                ("U", 83),
                ("L", 12),
                ("D", 49),
                ("R", 71),
                ("U", 7),
                ("L", 72),
            ],
            [
                ("U", 62),
                ("R", 66),
                ("U", 55),
                ("R", 34),
                ("D", 71),
                ("R", 55),
                ("D", 58),
                ("R", 83),
            ],
        ]
        self.assertEqual(partB(wires), 610)

    def test_run2b(self):
        wires = [
            [
                ("R", 98),
                ("U", 47),
                ("R", 26),
                ("D", 63),
                ("R", 33),
                ("U", 87),
                ("L", 62),
                ("D", 20),
                ("R", 33),
                ("U", 53),
                ("R", 51),
            ],
            [
                ("U", 98),
                ("R", 91),
                ("D", 20),
                ("R", 16),
                ("D", 67),
                ("R", 40),
                ("U", 7),
                ("R", 15),
                ("U", 6),
                ("R", 7),
            ],
        ]
        self.assertEqual(partB(wires), 410)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    args = parser.parse_args()

    wires = []
    with open(args.input) as fh:
        parts = [l.strip().split(",") for l in fh]
        for part in parts:
            wire = [(p[0], int(p[1:])) for p in part]
            wires.append(wire)

    print(partA(wires))
    print(partB(wires))
