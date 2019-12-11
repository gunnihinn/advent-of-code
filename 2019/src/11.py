import argparse
import collections
import enum
import itertools
import unittest

from src.vm import VM

class Direction(enum.Enum):
    N = 0
    E = 1
    S = 2
    W = 3

    def turn(self, lr):
        if lr == 0: # left
            return Direction((self.value - 1) % 4)
        else:
            return Direction((self.value + 1) % 4)

    def step(self):
        if self == Direction.N:
            return (0, 1)
        elif self == Direction.E:
            return (1, 0)
        elif self == Direction.S:
            return (0, -1)
        else:
            return (-1, 0)

def partA(codes):
    instructions = []
    vm = VM(codes, [0])

    grid = {}
    pos_x = 0
    pos_y = 0
    facing = Direction.N

    while True:
        vm.run()
        if len(vm._output) > 2:
            import pdb; pdb.set_trace()
            raise Exception("Got too much output")
        elif len(vm._output) == 2:
            paint, move = vm._output
            grid[(pos_x, pos_y)] = paint

            facing = facing.turn(move)
            x, y = facing.step()

            pos_x += x
            pos_y += y

            vm.inputs = [grid.get((pos_x, pos_y), 0)]
            vm._output = []
        else:
            break

    return len(grid)

def partB(codes):
    instructions = []
    vm = VM(codes, [1])

    grid = {}
    pos_x = 0
    pos_y = 0
    facing = Direction.N

    while True:
        vm.run()
        if len(vm._output) > 2:
            import pdb; pdb.set_trace()
            raise Exception("Got too much output")
        elif len(vm._output) == 2:
            paint, move = vm._output
            assert paint in {0, 1}
            grid[(pos_x, pos_y)] = paint

            facing = facing.turn(move)
            x, y = facing.step()

            pos_x += x
            pos_y += y

            vm.inputs = [grid.get((pos_x, pos_y), 0)]
            vm._output = []
        else:
            break

    x_m = min(pt[0] for pt in grid if grid[pt])
    y_m = min(pt[1] for pt in grid if grid[pt])
    painted = {(pt[0] - x_m, pt[1] - y_m) for pt, paint in grid.items() if paint}

    width = max(pt[0] for pt in painted) + 1
    height = max(pt[1] for pt in painted) + 1

    floor = []
    for _ in range(height):
        floor.append([0] * width)

    for pt in painted:
        floor[pt[1]][pt[0]] = 1

    floor.reverse()
    for row in floor:
        for pt in row:
            if pt == 1:
                print('x', end='')
            else:
                print(' ', end='')
        print('|\n', end='')

class TestProblem(unittest.TestCase):

    def test_run0(self):
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    with open(args.input) as fh:
        codes = [int(i) for i in fh.read().strip().split(',')]

    print(partA(codes))
    partB(codes)
