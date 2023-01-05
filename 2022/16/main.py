# /usr/bin/env python

import argparse
import collections
import copy
import functools
import itertools
import re
from typing import *

# The problem can be seen as being recursive.
# The answer for a graph G with starting node s with rate r and time t remaining is
#
#   P(G, s, r, t) = r * (t-1) + P(G, s, 0, t-1)
#
# and the answer for a graph G where *all* the nodes have rate 0 is 0.
# This may be enough to answer. If not we can estimate the maximum answer from
# the remaining time and positive nodes and prune by the best answer found so
# far. We can get a guess at a good starting answer by visiting nodes in the order of rates.


class Data:
    def __init__(self, graph, rates) -> None:
        self.graph = graph
        self.rates = rates

    def __str__(self) -> str:
        return f"{self.graph} - {self.rates}"


def parse(lines: List[str]) -> Data:
    re_valve = re.compile(
        r"Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.+)"
    )

    graph = {}
    rates = {}
    for line in lines:
        if m := re_valve.match(line):
            src = m.group(1)
            rate = int(m.group(2))
            targets = m.group(3).split(", ")
            rates[src] = rate
            graph[src] = targets
        else:
            raise Exception(f"Should have matched {line}")

    return Data(graph, rates)


def mmin(xs: List[int]) -> int:
    if xs:
        return min(xs)
    return 0


def dist(
    graph: Dict[str, List[str]], start: str, end: str, length=0, visited=None
) -> int:
    if start == end:
        return length

    visited = visited or []
    ds = [
        dist(graph, node, end, length + 1, visited + [node])
        for node in graph[start]
        if not node in visited
    ]

    return mmin([d for d in ds if d != 0])


def dist_all(graph: Dict[str, List[str]]) -> Dict[Tuple[str, str], int]:
    known = {}

    for a, b in itertools.product(graph, repeat=2):
        if len(known) == len(graph) ** 2:
            break
        if (a, b) in known:
            continue
        known[(a, b)] = dist(graph, a, b)
        known[(b, a)] = known[(a, b)]

    return known


def part1(data: Data) -> int:
    dists = dist_all(data.graph)
    rates = {k: v for k, v in data.rates.items() if v != 0}

    return P(dists, rates, "AA", 30)


def P(
    dists: Dict[Tuple[str, str], int],
    rates: Dict[str, int],
    pos: str,
    time: int,
) -> int:
    if not rates:
        return 0

    if time <= 0:
        return 0

    ps = []
    for node in rates:
        new_rates = {k: v for k, v in rates.items() if k != node}
        t = dists[(pos, node)]
        if time - t > 0:
            ps.append(
                (time - t - 1) * rates[node] + P(dists, new_rates, node, time - t - 1)
            )

    if not ps:
        return 0

    return max(ps)


def part2(data: Data) -> int:
    dists = dist_all(data.graph)
    rates = {k: v for k, v in data.rates.items() if v != 0}
    open = {}
    players = [("AA", 0, 0) for _ in range(1)]

    return Q(dists, rates, open, players, 30)


def Q(
    dists: Dict[Tuple[str, str], int],
    rates: Dict[str, int],
    open: Dict[str, int],
    players: List[Tuple[str, int, int]],
    time: int,
) -> int:
    if time <= 0:
        return 0

    total = sum(v for v in open.values())
    if not rates:
        return total * time

    pos, rate, wait = players[0]
    ps = []
    if wait == 0:
        new_open = copy.deepcopy(open)
        if rate > 0:
            new_open[pos] = rate
        for node in rates:
            new_rates = {k: v for k, v in rates.items() if k != node}
            t = dists[(pos, node)]
            ps.append(
                total
                + Q(dists, new_rates, new_open, [(node, rates[node], t - 1)], time - 1)
            )
    else:
        ps.append(total + Q(dists, rates, open, [(pos, rate, wait - 1)], time - 1))

    if not ps:
        return 0

    return max(ps)


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
