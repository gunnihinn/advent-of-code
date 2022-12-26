# /usr/bin/env python

import argparse
import collections
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
            for x in range(self.mx, self.Mx + 1):
                line.append(self.cave.get((x, y), "."))
            lines.append("".join(line))

        return "\n".join(lines)

    def inside(self, x, y):
        return self.mx <= x and x <= self.Mx and self.my <= y and y <= self.My

    def fall(self):
        x, y = self.orig
        while self.inside(x, y):
            if (x, y + 1) not in self.cave:
                y += 1
            elif (x - 1, y + 1) not in self.cave:
                x -= 1
                y += 1
            elif (x + 1, y + 1) not in self.cave:
                x += 1
                y += 1
            else:
                self.cave[(x, y)] = "o"
                return

        if not self.inside(x, y):
            raise Exception()


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
    i = 0
    while True:
        try:
            data.fall()
        except:
            break
        i += 1
    return i


def part2(data: Data) -> int:
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    with open(args.filename) as fh:
        data = parse(fh.readlines())

    p1 = part1(data)
    print(f"Part 1: {p1}")
    p2 = part2(data)
    print(f"Part 2: {p2}")
