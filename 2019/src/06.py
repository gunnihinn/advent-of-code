import argparse
import unittest

def partA(connections):
    orbits = tree(connections)
    hs = heights(orbits)
    return sum(hs.values())

def partB(codes):
    pass

def tree(connections):
    orbits = {}
    for source, satellite in connections:
        assert satellite not in orbits
        orbits[satellite] = source

    return orbits

def heights(orbits):
    hs = {}
    origins = orbits.values() - orbits.keys()
    for o in origins:
        hs[o] = 0

    while len(hs) < len(orbits.values()):
        todo = orbits.keys() - hs.keys()
        for satellite in todo:
            source = orbits[satellite]
            if source in hs:
                hs[satellite] = hs[source] + 1

    return hs


class TestProblem(unittest.TestCase):

    def test_run1(self):
        lines = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L""".split('\n')
        conns = [line.strip().split(')') for line in lines]
        orbits = tree(conns)
        hs = heights(orbits)
        self.assertEqual(partA(conns), 42)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    with open(args.input) as fh:
        connections = [line.strip().split(')') for line in fh]

    print(partA(connections))
    print(partB(connections))
