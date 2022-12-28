# /usr/bin/env python

import argparse
import collections
import copy
import functools
import itertools
import re
from typing import *


class Sensor:
    def __init__(self, xy, beacon, r) -> None:
        self.xy = xy
        self.beacon = beacon
        self.r = r

    def __str__(self) -> str:
        return f"{self.xy} - {self.r}"

    def inside(self, x, y) -> bool:
        return abs(self.xy[0] - x) + abs(self.xy[1] - y) <= self.r

    def inside_points(self, y):
        z, w = self.xy
        r = self.r - abs(w - y)
        # |x - z| <= self.r - |w - y|
        return ((t, y) for t in range(-(r - z), r + z + 1))

    def buffer(self, length=1):
        for wy in range(0, self.r + length + 1):
            w0 = wy + self.xy[1]
            w1 = self.xy[1] - wy
            yield (self.r + length - wy + self.xy[0], w0)
            yield (-(self.r + length - wy) + self.xy[0], w0)


class Data:
    def __init__(self, sensors: List[Sensor]) -> None:
        self.sensors = sensors

    def __str__(self):
        return "\n".join(str(s) for s in self.sensors)

    def in_cover(self, x, y) -> bool:
        return any(s.inside(x, y) for s in self.sensors)


def parse(lines: List[str]) -> Data:
    re_sensor = re.compile(
        r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
    )

    sensors = []
    for line in lines:
        if m := re_sensor.match(line):
            xy = (int(m.group(1)), int(m.group(2)))
            pq = (int(m.group(3)), int(m.group(4)))
            r = abs(pq[0] - xy[0]) + abs(pq[1] - xy[1])
            sensors.append(Sensor(xy, pq, r))
        else:
            raise Exception(f"Line '{line}' didn't match")

    return Data(sensors)


def part1(data: Data, is_test: bool) -> int:
    ps = set()
    y = 10 if is_test else 2000000
    for sensor in data.sensors:
        ps = ps.union(sensor.inside_points(y=y))

    ps = ps.difference(s.beacon for s in data.sensors)

    return len(ps)


def part2(data: Data, is_test: bool) -> int:
    n = 20 if is_test else 4000000

    def valid(z, w):
        return 0 <= z and z <= n and 0 <= w and w <= n

    for sensor in data.sensors:
        for z, w in sensor.buffer():
            if valid(z, w) and not data.in_cover(z, w):
                return z * 4000000 + w


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    with open(args.filename) as fh:
        data = parse(fh.readlines())

    is_test = not "input" in args.filename

    # p1 = part1(copy.deepcopy(data), is_test)
    # print(f"Part 1: {p1}")
    p2 = part2(copy.deepcopy(data), is_test)
    print(f"Part 2: {p2}")
