import argparse
import unittest

def partA(lines):
    c = 0
    for line in lines:
        c += 2
        c += len(line)
        c -= count(line)

    return c

def partB(lines):
    c = 0

    for line in lines:
        c += 4
        c -= len(line)
        for char in line:
            if char == '\\':
                c += 1
            elif char == '"':
                c += 1
            c += 1

    return c

def count(line):
    stack = list(line)
    stack.reverse()

    count = 0
    while stack:
        c = stack.pop()
        if c == '\\':
            c = stack.pop()
            if c == 'x':
                stack.pop()
                stack.pop()
                count += 1
            else:
                count += 1
        else:
            count += 1

    return count

class TestProblem(unittest.TestCase):

    def test_count(self):
        self.assertEqual(count(r''), 0)
        self.assertEqual(count(r'abc'), 3)
        self.assertEqual(count(r'aaa\"aaa'), 7)
        self.assertEqual(count(r'\x27'), 1)

    def test_a(self):
        lines = [
            r'',
            r'abc',
            r'aaa\"aaa',
            r'\x27',
        ]
        self.assertEqual(partA(lines), 12)
        self.assertEqual(partB(lines), 19)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    with open(args.input) as fh:
        lines = [l.strip()[1:-1] for l in fh]

    print(partA(lines))
    print(partB(lines))
