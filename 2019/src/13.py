import argparse
import collections
import enum
import time
import itertools
import unittest

from src.vm import VM


def partA(codes):
    vm = VM(codes)
    vm.run()
    
    assert len(vm._output) % 3 == 0
    moves = []
    for i in range(0, len(vm._output) // 3):
        moves.append((vm._output[3*i], vm._output[3*i+1], vm._output[3*i+2]))

    render(moves)

    blocks = 0
    for move in moves:
        if move[2] == 2:
            blocks += 1

    return blocks

def partB(codes):
    vm = VM(codes)
    vm._codes[0] = 2
    vm.run()

    ms = moves(vm._output)
    ball, paddle = positions(ms)
    pball = None
    render(ms)

    while bricks(ms):
        if pball is None:
            l = 0
        elif ball[0] == paddle[0]:
            l = 0
        else:
            dx = ball[0] - pball[0]
            next_x = ball[0] + dx
            if next_x < paddle[0]:
                l = -1
            elif next_x == paddle[0]:
                l = 0
            else:
                l = 1

        inputs = [l]

        vm.inputs = inputs
        vm.run()
        ms = moves(vm._output)
        render(ms)

        pball = ball
        ball, paddle = positions(ms)
        assert paddle[1] >= ball[1]

def bricks(moves):
    c = 0
    for x, y, m in moves:
        if m == 2:
            c += 1

    return c


def positions(ms):
    ball = None
    paddle = None

    for x, y, m in ms:
        if m == 4:
            ball = (x, y)
        elif m == 3:
            paddle = (x, y)

    return ball, paddle

def moves(output):
    assert len(output) % 3 == 0
    moves = []
    for i in range(0, len(output) // 3):
        moves.append((output[3*i], output[3*i+1], output[3*i+2]))

    print(moves[-2])
    print(moves[-1])

    return moves


def render(board):
    max_x = max(b[0] for b in board) + 1
    max_y = max(b[1] for b in board) + 1

    screen = []
    for _ in range(max_y):
        screen.append([' '] * max_x)

    for x, y, m in board:
        if m == 0:
            screen[y][x] = ' '
        elif m == 1:
            screen[y][x] = 'W'
        elif m == 2:
            screen[y][x] = 'B'
        elif m == 3:
            screen[y][x] = 'P'
        elif m == 4:
            screen[y][x] = 'O'

    for row in screen:
        print(''.join(row))

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
