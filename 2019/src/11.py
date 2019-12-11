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
    while True:
        vm.run()
        if len(vm._output) > 2:
            import pdb; pdb.set_trace()
            raise Exception("Got too much output")
        elif len(vm._output) == 2:
            instructions.append(vm._output)
            vm.inputs = [vm._output[0]]
            vm._output = []
        else:
            break

    return paint(instructions)

def paint(instructions):
    grid = {(0, 0)}
    pos_x = 0
    pos_y = 0
    facing = Direction.N
    for _, move in instructions:
        x, y = facing.step()
        facing = facing.turn(move)
        pos_x += x
        pos_y += y
        grid.add((pos_x, pos_y))

    return len(grid)

def partB(codes):
    vm = VM(codes, [2])
    vm.run()
    return vm.output


class TestProblem(unittest.TestCase):

    def test_run0(self):
        ins = [
            [1, 0],
            [0, 0],
            [1, 0],
            [1, 0],
            [0, 1],
            [1, 0],
            [1, 0],
        ]
        exp = 6
        got = paint(ins)
        assert got == exp


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    with open(args.input) as fh:
        codes = [int(i) for i in fh.read().strip().split(',')]

    print(partA(codes))
    #print(partB(codes))
