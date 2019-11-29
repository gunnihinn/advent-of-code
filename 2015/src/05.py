import argparse
import re
import unittest


def partA(lines):
    return sum(nice(l) for l in lines)

def partB(seed):
    return sum(nice2(l) for l in lines)

def nice(line):
    if 'ab' in line:
        return False
    elif 'cd' in line:
        return False
    elif 'pq' in line:
        return False
    elif 'xy' in line:
        return False

    double = 0
    for a, b in zip(line, line[1:]):
        if a == b:
            double += 1

    wovels = 0
    ws = {'a', 'e', 'i', 'o', 'u'}
    for a in line:
        if a in ws:
            wovels += 1

    return double and (wovels >= 3)


def nice2(line):
    return re.search(r'(..).*\1', line) is not None \
            and \
            re.search(r'(.).\1', line) is not None


class TestProblem(unittest.TestCase):

    def test_nice(self):
        self.assertTrue(nice('ugknbfddgicrmopn'))
        self.assertTrue(nice('aaa'))
        self.assertFalse(nice('jchzalrnumimnmhp'))
        self.assertFalse(nice('haegwjzuvuyypxyu'))
        self.assertFalse(nice('dvszwmarrgswjxmb'))

    def test_nice2(self):
        self.assertTrue(nice2('qjhvhtzxzqqjkmpb'))
        self.assertTrue(nice2('xxyxx'))
        self.assertFalse(nice2('uurcxstgmygtbstg'))
        self.assertFalse(nice2('ieodomkazucvgmuy'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    with open(args.input) as fh:
        lines = [l.strip() for l in fh]

    print(partA(lines))
    print(partB(lines))
