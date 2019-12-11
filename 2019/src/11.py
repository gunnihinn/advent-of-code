import argparse
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
            grid[(pos_x, pos_y)] = paint

            facing = facing.turn(move)
            x, y = facing.step()

            pos_x += x
            pos_y += y

            vm.inputs = [grid.get((pos_x, pos_y), 0)]
            vm._output = []
        else:
            break
    y_m = min(pt[1] for pt in grid)
    grid = {(pt[0], pt[1] - y_m) for pt, paint in grid.items() if paint}

    x_m, x_M = min(pt[0] for pt in grid), max(pt[0] for pt in grid)
    y_m, y_M = min(pt[1] for pt in grid), max(pt[1] for pt in grid)

    width = x_M - x_m + 1
    height = y_M - y_m + 1
    floor = [[0] * width] * height

    with open('pts.txt', 'w') as fh:
        for x, y in grid:
            print('{},{}'.format(x,y), file=fh)

    for x, y in grid:
        floor[y - y_m][x - x_m] = 1

    #import pdb; pdb.set_trace()
    for row in floor:
        for pt in row:
            out = 'x' if pt else ' '
            print(out, end='')
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
