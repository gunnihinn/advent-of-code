import argparse
import unittest

def partA(connections):
    orbits = tree(connections)
    hs = heights(orbits)
    return sum(hs.values())

def partB(connections):
    orbits = tree(connections)

    orbits_you = orbits_of(orbits, 'YOU')
    orbits_san = orbits_of(orbits, 'SAN')
    common = first_common(orbits_you, orbits_san)
    new = prune(orbits, common)
    hs = heights(new)

    return hs['YOU'] + hs['SAN'] - 2

def prune(orbits, source):
    new = {}
    for sat in orbits:
        objs = set(orbits_of(orbits, sat))
        if source in objs:
            new[sat] = orbits[sat]

    return new

def first_common(orbits_a, orbits_b):
    orbits_a.reverse()
    orbits_b.reverse()
    assert orbits_a[0] == orbits_b[0]
    for a, b in zip(orbits_a, orbits_b):
        if a == b:
            pt = a
        else:
            return pt

def orbits_of(orbits, pt):
    orbs = []

    while True:
        source = orbits.get(pt, None)
        if source is not None:
            orbs.append(source)
            pt = source
        else:
            break

    return orbs

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

    def test_run2(self):
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
        self.assertEqual(partA(conns), 42)

    def test_run2(self):
        liness = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN""".split('\n')
        connss = [line.strip().split(')') for line in liness]
        self.assertEqual(partB(connss), 4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    with open(args.input) as fh:
        connections = [line.strip().split(')') for line in fh]

    print(partA(connections))
    print(partB(connections))
