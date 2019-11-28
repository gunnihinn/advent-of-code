import argparse
import unittest

def paper(l, w, h):
    return 2 * l * w + 2 * w * h + 2 * h * l + min(l * w, w * h, h * l)

def ribbon(l, w, h):
    return 2 * min(l + w, l + h, w + h) + l * w * h

def partA(dimensions):
    total = 0
    for l, w, h in dimensions:
        total += paper(l, w, h)

    return total

def partB(dimensions):
    total = 0
    for l, w, h in dimensions:
        total += ribbon(l, w, h)

    return total


class TestProblem(unittest.TestCase):

    def test_paper(self):
        self.assertEqual(paper(2, 3, 4), 58)
        self.assertEqual(paper(1, 1, 10), 43)

    def test_ribbon(self):
        self.assertEqual(ribbon(2, 3, 4), 34)
        self.assertEqual(ribbon(1, 1, 10), 14)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    with open(args.input) as fh:
        dimensions = [tuple(map(int, line.split('x'))) for line in fh]

    print(partA(dimensions))
    print(partB(dimensions))
