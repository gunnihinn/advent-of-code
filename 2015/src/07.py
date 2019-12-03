import argparse
import collections
import enum
import re
import unittest

_mask = (1 << 16) - 1

class Op(enum.Enum):
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    LSHIFT = "LSHIFT"
    RSHIFT = "RSHIFT"
    SET = "SET"

    def apply(self, wires, a, b=None):
        if self is Op.NOT or self is Op.SET:
            assert b is None
        else:
            assert b is not None

        if self is not Op.SET and isinstance(a, str):
            a = wires[a]
            assert isinstance(a, int)
        if b is not None and isinstance(b, str):
            b = wires[b]
            assert isinstance(b, int)

        if self is Op.AND:
            return a & b
        elif self is Op.OR:
            return a | b
        elif self is Op.NOT:
            return (~a) & _mask
        elif self is Op.LSHIFT:
            return (a << b) & _mask
        elif self is Op.SET:
            wires[a] = b
        else:
            return a >> b


def intify(x):
    try:
        return int(x)
    except:
        return x

def parse(lines):
    wires = collections.defaultdict(int)
    ops = []

    for line in lines:
        parts = [intify(p) for p in line.split(' ')]
        if parts[1] == '->':
            ops.append((parts[2], Op.SET, parts[0]))
        elif parts[0] == 'NOT':
            ops.append((parts[3], Op(parts[0]), parts[1]))
        else:
            ops.append((parts[4], Op(parts[1]), parts[0], parts[2]))

    return wires, ops


def run(wires, ops):
    for op in ops:
        out, o, *args = op
        wires[out] = o.apply(wires, *args)

    return wires


def partA(lines):
    wires, ops = parse(lines)
    got = run(wires, ops)
    return got['a']

def partB(seed):
    pass

class TestProblem(unittest.TestCase):

    def test_A(self):
        lines = """123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i""".split('\n')

        wires, ops = parse(lines)
        got = run(wires, ops)
        exp = {
            'd': 72,
            'e': 507,
            'f': 492,
            'g': 114,
            'h': 65412,
            'i': 65079,
            'x': 123,
            'y': 456,
        }

        print(got)
        print(exp)

        self.assertEqual(got, exp)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    with open(args.input) as fh:
        lines = [l.strip() for l in fh]

    print(partA(lines))
    #print(partB(lines))
