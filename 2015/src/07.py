import argparse
import enum
import unittest

_mask = (1 << 16) - 1

class Op(enum.Enum):
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    LSHIFT = "LSHIFT"
    RSHIFT = "RSHIFT"

    def apply(self, a: int, b: int=None) -> int:
        if self is Op.NOT:
            assert b is None
        else:
            assert b is not None

        if self is Op.AND:
            return a & b
        elif self is Op.OR:
            return a | b
        elif self is Op.NOT:
            return (~a) & _mask
        elif self is Op.LSHIFT:
            return (a << b) & _mask
        else:
            return a >> b


def intify(x):
    try:
        return int(x)
    except:
        return x

def partA(lines):
    registers = init(lines)
    done = forward_eval(registers)
    return done['a']

def partB(seed):
    registers = init(lines)
    done = forward_eval(registers)
    registers['b'] = done['a']
    done = forward_eval(registers)
    return done['a']

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

        registers = init(lines)
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

        got = forward_eval(registers)
        self.assertEqual(got, exp)


def init(lines):
    registers = {}
    for line in lines:
        left, right = line.split(' -> ')
        assert right not in registers
        registers[right] = intify(left)

    return registers


def forward_eval(registers):
    done = {}
    c = -1
    while len(done) != c:
        c = len(done)
        done = step(registers, done)

    return done

def step(registers, done):
    if not done:
        done = { k: v for k, v in registers.items() if isinstance(v, int) }

    for k in registers.keys() - done.keys():
        args = [intify(x) for x in registers[k].split(' ')]
        assert 0 < len(args) and len(args) <= 3

        if len(args) == 1:
            a = args[0]
            if a in done:
                done[k] = done[a]
        elif len(args) == 2:
            assert args[0] == 'NOT'
            op = Op(args[0])
            a = args[1]
            if a in done:
                a = done[a]
            if isinstance(a, int):
                done[k] = op.apply(a)
        else:
            op = Op(args[1])
            a, b = args[0], args[2]
            if a in done:
                a = done[a]
            if b in done:
                b = done[b]
            if isinstance(a, int) and isinstance(b, int):
                done[k] = op.apply(a, b)

    return done


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    with open(args.input) as fh:
        lines = [l.strip() for l in fh]

    print(partA(lines))
    print(partB(lines))
