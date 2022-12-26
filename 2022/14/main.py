# /usr/bin/env python

import argparse
import collections
import copy
import functools
from typing import *


class Data:
    def __init__(self) -> None:
        self.cave: Dict[Tuple[int, int], bool] = {}
        self.mx: int = 0
        self.Mx: int = 0
        self.my: int = 0
        self.My: int = 0
        self.orig = (500, 0)

    def __str__(self):
        lines = []
        for y in range(self.my, self.My + 1):
            line = []
            for x in range(500 - 20, 500 + 20 + 1):
                line.append(self.cave.get((x, y), "."))
            lines.append("".join(line))

        return "\n".join(lines)

    def blocked(self, x, y):
        return (x, y) in self.cave

    def inside(self, x, y):
        return self.mx <= x and x <= self.Mx and self.my <= y and y <= self.My

    def fall(self):
        x, y = self.orig
        while self.inside(x, y):
            if not self.blocked(x, y + 1):
                y += 1
            elif not self.blocked(x - 1, y + 1):
                x -= 1
                y += 1
            elif not self.blocked(x + 1, y + 1):
                x += 1
                y += 1
            else:
                self.cave[(x, y)] = "o"
                return

            if self.orig in self.cave:
                raise Exception()

        if not self.inside(x, y):
            raise Exception()

    def size(self):
        return sum(v == "o" for v in self.cave.values())


def sign(x: int) -> int:
    if x > 0:
        return 1
    elif x == 0:
        return 0
    else:
        return -1


def rng(p: Tuple[int, int], q: Tuple[int, int]):
    dx = sign(q[0] - p[0])
    dy = sign(q[1] - p[1])

    x, y = p
    stop = False
    while True:
        yield (x, y)
        x += dx
        y += dy
        if stop:
            break
        stop = (x, y) == q


def parse(lines: List[str]) -> List[Data]:
    paths = []
    for line in lines:
        path = []
        parts = line.split(" -> ")
        for part in parts:
            x, y = part.split(",")
            path.append((int(x), int(y)))
        paths.append(path)

    data = Data()
    for path in paths:
        for s, e in zip(path, path[1:]):
            for p in rng(s, e):
                data.cave[p] = "#"

    data.mx = min(k[0] for k in data.cave.keys())
    data.Mx = max(k[0] for k in data.cave.keys())
    data.my = min(min(k[1] for k in data.cave.keys()), 0)
    data.My = max(k[1] for k in data.cave.keys())

    return data


def part1(data: Data) -> int:
    while True:
        try:
            data.fall()
        except:
            break
    return data.size()


def part2(data: Data) -> int:
    for x in range(-10000, 10000):
        data.cave[(x, data.My + 2)] = "#"
    data.My += 2
    data.mx = min(k[0] for k in data.cave)
    data.Mx = max(k[0] for k in data.cave)

    a = len(data.cave)
    b = 0
    while a != b:
        try:
            data.fall()
            a = b
            b = len(data.cave)
        except:
            break
    return data.size()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    with open(args.filename) as fh:
        data = parse(fh.readlines())

    p1 = part1(copy.deepcopy(data))
    print(f"Part 1: {p1}")
    p2 = part2(copy.deepcopy(data))
    print(f"Part 2: {p2}")
