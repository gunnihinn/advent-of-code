# /usr/bin/env python

import argparse
import functools
from typing import *


class Packet:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children

    @staticmethod
    def parse(line: str):
        if not line:
            return Packet(), None

        if line[0] == "[":
            c = 1
            i = 0
            while c > 0:
                i += 1
                if line[i] == "[":
                    c += 1
                elif line[i] == "]":
                    c -= 1
            pre = line[1:i]
            post = line[i + 2 :]

            children = []
            while pre:
                p, pre = Packet.parse(pre)
                children.append(p)

            return Packet(children=children), post

        idx = line.find(",")
        if idx == -1:
            return Packet(val=int(line)), None
        else:
            return Packet(val=int(line[0:idx])), line[idx + 1 :]

    def __str__(self) -> str:
        if self.val is not None:
            return f"{self.val}"
        return "[{}]".format(",".join((p.__str__() for p in self.children)))

    def lt(self, other):
        if self.val is not None and other.val is not None:
            if self.val == other.val:
                return None
            return self.val < other.val

        elif self.val is not None and other.val is None:
            return Packet(children=[self]).lt(other)

        elif self.val is None and other.val is not None:
            return self.lt(Packet(children=[other]))

        else:
            for a, b in zip(self.children, other.children):
                if (ok := a.lt(b)) is not None:
                    return ok

            if len(self.children) == len(other.children):
                return None
            else:
                return len(self.children) < len(other.children)

    def __eq__(self, other):
        if self.val is not None and other.val is not None:
            return self.val == other.val

        elif self.val is not None and other.val is None:
            return False

        elif self.val is None and other.val is not None:
            return False

        else:
            for a, b in zip(self.children, other.children):
                if not a == b:
                    return False

            return len(self.children) == len(other.children)


def parse(lines: List[str]) -> List[Packet]:
    lines = [l.strip() for l in lines if l.strip()]

    packets = []
    for a, b in zip(lines[0::2], lines[1::2]):
        p, _ = Packet.parse(a)
        q, _ = Packet.parse(b)
        packets.append((p, q))

    return packets


def part1(data):
    total = 0
    i = 0
    for p, q in data:
        i += 1
        ok = p.lt(q)
        assert ok is not None
        total += ok * i
    return total


def part2(data):
    a, _ = Packet.parse("[[2]]")
    b, _ = Packet.parse("[[6]]")

    packets = [a, b]
    for p, q in data:
        packets.append(p)
        packets.append(q)

    # yay bubbles
    i = 0
    while i < len(packets):
        for j in range(i + 1, len(packets)):
            if not packets[i].lt(packets[j]):
                packets[i], packets[j] = packets[j], packets[i]
                break
        else:
            i += 1

    ia = 0
    ib = 0
    for i in range(len(packets)):
        if packets[i] == a:
            ia = i + 1
        elif packets[i] == b:
            ib = i + 1

    return ia * ib


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
