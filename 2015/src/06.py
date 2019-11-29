import argparse
import re
import unittest


def partA(lines):
    grid = [[0] * 1000 for _ in range(1000)]

    for line in lines:
        m = re.search(r'(\d+),(\d+) through (\d+),(\d+)', line)
        assert m is not None
        x1 = int(m.group(1))
        y1 = int(m.group(2))
        x2 = int(m.group(3))
        y2 = int(m.group(4))

        if line.startswith('turn on'):
            for x in range(x1, x2+1):
                for y in range(y1, y2+1):
                    grid[x][y] = 1
        elif line.startswith('turn off'):
            for x in range(x1, x2+1):
                for y in range(y1, y2+1):
                    grid[x][y] = 0
        elif line.startswith('toggle'):
            for x in range(x1, x2+1):
                for y in range(y1, y2+1):
                    grid[x][y] = not grid[x][y] 
        else:
            raise Exception("Bad line '{}'".format(line))

    return sum(sum(xs) for xs in grid)

def partB(seed):
    grid = [[0] * 1000 for _ in range(1000)]

    for line in lines:
        m = re.search(r'(\d+),(\d+) through (\d+),(\d+)', line)
        assert m is not None
        x1 = int(m.group(1))
        y1 = int(m.group(2))
        x2 = int(m.group(3))
        y2 = int(m.group(4))

        if line.startswith('turn on'):
            for x in range(x1, x2+1):
                for y in range(y1, y2+1):
                    grid[x][y] += 1
        elif line.startswith('turn off'):
            for x in range(x1, x2+1):
                for y in range(y1, y2+1):
                    grid[x][y] = max(grid[x][y] - 1, 0)
        elif line.startswith('toggle'):
            for x in range(x1, x2+1):
                for y in range(y1, y2+1):
                    grid[x][y] += 2
        else:
            raise Exception("Bad line '{}'".format(line))

    return sum(sum(xs) for xs in grid)


class TestProblem(unittest.TestCase):

    def test_nice(self):
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    with open(args.input) as fh:
        lines = [l.strip() for l in fh]

    print(partA(lines))
    print(partB(lines))
