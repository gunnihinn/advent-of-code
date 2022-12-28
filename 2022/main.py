# /usr/bin/env python

import argparse
import collections
import copy
import functools
import itertools
import re
from typing import *


class Data:
    pass


def parse(lines: List[str]) -> Data:
    return Data()


def part1(data: Data) -> int:
    result = 0
    return result


def part2(data: Data) -> int:
    result = 0
    return result


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
