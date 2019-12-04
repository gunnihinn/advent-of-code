import argparse
import collections
import unittest


def partA(start, end):
    return sum(rule_a(n) for n in range(start, end+1))

def partB(start, end):
    return sum(rule_a(n) and rule_b(n) for n in range(start, end+1))

def rule_a(n):
    ds = digits(n)

    return all((
        len(ds) == 6,
        any(n == m for n, m in zip(ds, ds[1:])),
        all(n <= m for n, m in zip(ds, ds[1:])),
    ))

def rule_b(n):
    ds = digits(n)
    c = collections.Counter(ds)

    return any(v == 2 for v in c.values())

def digits(n):
    assert n > 0
    ds = []
    while n:
        d = n % 10
        n = n // 10
        ds.append(d)
    ds.reverse()

    return ds

class TestProblem(unittest.TestCase):
    def test_digits(self):
        n = 123456
        self.assertEqual(digits(n), [1, 2, 3, 4, 5, 6])

    def test_a(self):
        self.assertTrue(rule_a(111111))
        self.assertFalse(rule_a(223450))
        self.assertFalse(rule_a(123789))

    def test_b(self):
        self.assertTrue(rule_b(112233))
        self.assertFalse(rule_b(123444))
        self.assertTrue(rule_b(111122))
        self.assertFalse(rule_b(111123))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    args = parser.parse_args()

    wires = []
    with open(args.input) as fh:
        start, end = list(map(int, fh.read().strip().split('-')))

    print(partA(start, end))
    print(partB(start, end))
