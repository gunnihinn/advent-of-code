# /usr/bin/env python

import argparse
import collections
import copy
import functools
import itertools
import math
import os.path
import pickle
import re
from typing import *


class Data:
    def __init__(self, graph, rates) -> None:
        self.graph = graph
        self.rates = rates

    def __str__(self) -> str:
        return f"{self.graph} - {self.rates}"

    def graphviz(self) -> str:
        nodes = set()
        for start in self.graph:
            for end in self.graph[start]:
                if not (start, end) in nodes and not (end, start) in nodes:
                    nodes.add((start, end))

        lines = []
        lines.append("graph {")

        for a, b in nodes:
            lines.append(f"  {a} -- {b}")

        lines.append('AA [color="red"]')
        for node, rate in self.rates.items():
            if rate != 0:
                lines.append(f'{node} [label="{node} ({rate})",color="blue"]')

        lines.append("}")

        return "\n".join(lines)


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


def oncemore(
    dists: Dict[Tuple[str, str], int],
    rates: Dict[str, int],
    visited: List[str],
    to_visit: List[str],
    time: int,
    score: int,
    best: int,
):
    # Assume dists has been +1'd
    if not to_visit or time <= 0:
        return score

    if score + sup(rates, [visited[-1]] + to_visit, time) < best:
        return score

    cur = visited[-1]
    for n in to_visit:
        tv = [m for m in to_visit if m != n]
        t = time - dists[(cur, n)]
        ns = score + max(time - dists[(cur, n)], 0) * rates[n]
        best = max(oncemore(dists, rates, visited + [n], tv, t, ns, best), best)

    return best


def part1(data: Data) -> int:
    N = len(data.rates)
    fn = f"./.dists-{N}.pkl"
    if os.path.exists(fn):
        with open(fn, mode="rb") as fh:
            dists = pickle.load(fh)
    else:
        dists = dist_all(data.graph)
        with open(fn, mode="wb") as fh:
            pickle.dump(dists, fh)
    rates = {k: v for k, v in data.rates.items() if v != 0}
    dists = {k: v + 1 for k, v in dists.items()}

    return oncemore(dists, rates, ["AA"], list(rates.keys()), 30, 0, 0)


def sup(rates: Dict[str, int], path: List[str], time: int) -> int:
    # Best possible outcome of this path if we're allowed to reorder it and assume all nodes are next to each other
    vals = sorted([rates.get(n, 0) for n in path], reverse=True)
    return sum(r * (time - t) for t, r in enumerate(vals, start=1))


def part2(data: Data) -> int:
    N = len(data.rates)
    fn = f"./.dists-{N}.pkl"
    if os.path.exists(fn):
        with open(fn, mode="rb") as fh:
            dists = pickle.load(fh)
    else:
        dists = dist_all(data.graph)
        with open(fn, mode="wb") as fh:
            pickle.dump(dists, fh)
    rates = {k: v for k, v in data.rates.items() if v != 0}
    dists = {k: v + 1 for k, v in dists.items()}

    p1 = oncemore(dists, rates, ["AA"], list(rates.keys()), 30, 0, 0)

    results = []
    for i in range(1, len(rates)):
        m = math.factorial(len(rates)) // math.factorial(i)
        print(f"Checking {m} combinations of length {i}")
        for sub in itertools.combinations(rates, i):
            compl = [n for n in rates if n not in sub]
            s1 = oncemore(dists, rates, ["AA"], list(sub), 26, 0, 0)
            s2 = oncemore(dists, rates, ["AA"], list(compl), 26, 0, p1 - s1)
            results.append(s1 + s2)

    return max(results)


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
