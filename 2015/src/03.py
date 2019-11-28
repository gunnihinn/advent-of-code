import argparse
import enum
import unittest

class Direction(enum.Enum):
    N = '^'
    E = '>'
    S = 'v'
    W = '<'

    def step(self):
        if self is Direction.N:
            return (1, 0)
        elif self is Direction.E:
            return (0, 1)
        elif self is Direction.S:
            return (-1, 0)
        elif self is Direction.W:
            return (0, -1)
        else:
            raise Exception("Unknown enum value")


def partA(directions):
    pt = (0, 0)
    houses = {pt}
    for d in directions:
        s = d.step()
        pt = (pt[0] + s[0], pt[1] + s[1])
        houses.add(pt)

    return len(houses)

def partB(directions):
    pt = (0, 0)
    houses = {pt}

    for d in directions[::2]:
        s = d.step()
        pt = (pt[0] + s[0], pt[1] + s[1])
        houses.add(pt)

    pt = (0, 0)
    for d in directions[1::2]:
        s = d.step()
        pt = (pt[0] + s[0], pt[1] + s[1])
        houses.add(pt)

    return len(houses)


class TestProblem(unittest.TestCase):

    def test_A1(self):
        src = '>'
        dirs = [Direction(c) for c in src]
        self.assertEqual(partA(dirs), 2)

    def test_A2(self):
        src = '^>v<'
        dirs = [Direction(c) for c in src]
        self.assertEqual(partA(dirs), 4)

    def test_A3(self):
        src = '^v^v^v^v^v'
        dirs = [Direction(c) for c in src]
        self.assertEqual(partA(dirs), 2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    with open(args.input) as fh:
        directions = [Direction(c) for line in fh for c in line]

    print(partA(directions))
    print(partB(directions))
