import argparse
import collections
import itertools
import unittest

def digit_counter(d):
    return lambda layer: sum(px == d for row in layer for px in row)

def partA(layers):
    layer = min(layers, key=digit_counter(0))
    return digit_counter(1)(layer) * digit_counter(2)(layer)

def partB(layers):
    screen = render(layers)
    assert digit_counter(2)(screen) == 0

    for h, row in enumerate(screen):
        for w, px in enumerate(row):
            if px == 1:
                print('x', end='')
            else:
                print(' ', end='')
        print('\n', end='')

def parse(blob, h, w):
    digits = [int(i) for i in blob.strip()]
    n = len(digits) // (h * w)
    layers = []
    while digits:
        layer = []
        for _ in range(h):
            row, digits = digits[0:w], digits[w:]
            assert len(row) == w
            layer.append(row)
        assert len(layer) == h
        layers.append(layer)

    assert len(layers) == n

    return layers

def render(layers):
    screen = layers.pop()

    while layers:
        layer = layers.pop()
        for h, row in enumerate(layer):
            for w, px in enumerate(row):
                if px != 2:
                    screen[h][w] = px

    return screen


class TestProblem(unittest.TestCase):

    def test_run1(self):
        layers = parse('123456789012', 2, 3)
        assert layers == [
            [[1, 2, 3], [4, 5, 6]],
            [[7, 8, 9], [0, 1, 2]],
        ]

        d1 = digit_counter(1)
        assert d1(layers[0]) == 1
        assert d1(layers[1]) == 1

    def test_run2(self):
        layers = parse('0222112222120000', 2, 2)
        assert layers == [
            [[0, 2], [2, 2]],
            [[1, 1], [2, 2]],
            [[2, 2], [1, 2]],
            [[0, 0], [0, 0]],
        ]

        screen = render(layers)
        assert screen == [[0, 1], [1, 0]]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    with open(args.input) as fh:
        layers = parse(fh.read(), h=6, w=25)

    print(partA(layers))
    partB(layers)
