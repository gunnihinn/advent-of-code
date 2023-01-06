# /usr/bin/env python

import argparse
import collections
import copy
import functools
import itertools
import math
import multiprocessing
import os.path
import pickle
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


def part1_calc_given_path(
    dists: Dict[Tuple[str, str], int], rates: Dict[str, str], path: List[str], time: int
) -> int:
    total = 0

    for a, b in zip(path, path[1:]):
        time -= dists[(a, b)] + 1
        if time < 0:
            break
        total += time * rates[b]
        assert time >= 0

    return total


def part1_alt(data: Data) -> int:
    dists = dist_all(data.graph)
    rates = {k: v for k, v in data.rates.items() if v != 0}

    M = None
    p = None
    for path in itertools.permutations(rates.keys()):
        m = part1_calc_given_path(dists, rates, ("AA",) + path, 30)
        if M is None or M < m:
            M = m
            p = path

    p = ("AA",) + p
    print(f"Path: {p}")
    return M


def part2_alt(data: Data) -> int:
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

    M = None
    p = None

    n = sum(
        math.factorial(len(rates)) * math.factorial(len(rates) - k) // math.factorial(k)
        for k in range(1, len(rates))
    )
    print(f"Checking up to {n} path combinations")

    i = 0
    j = 0
    for l in range(len(rates) // 2, 0, -1):
        for path1 in itertools.permutations(rates.keys(), l):
            nodes2 = [n for n in rates if n not in path1]
            for path2 in itertools.permutations(nodes2):
                if j % 100000 == 0:
                    print(f"... checked {i}/{n} paths, best so far {M}")

                j += 1
                m1 = part1_calc_given_path(dists, rates, ("AA",) + path1, 26)

                s = sup(rates, path2, 26)
                if M is not None and m1 + s < M:
                    i += math.factorial(len(nodes2))
                    break

                i += 1
                m2 = part1_calc_given_path(dists, rates, ("AA",) + path2, 26)
                if M is None or M < m1 + m2:
                    M = m1 + m2
                    p = (("AA",) + path1, ("AA",) + path2)

    print(f"... checked {i}/{n} paths, best so far {M}")

    print(f"Paths: {p}")
    return M


def part2_alt_multithread(data: Data, l: int, tid: int) -> int:
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

    M = None
    p = None

    n = math.factorial(len(rates))
    print(f"Thread {tid}: Checking {n} path combinations")

    i = 0
    j = 0
    for path1 in itertools.permutations(rates.keys(), l):
        if length(dists, path1) > 26:
            i += math.factorial(len(rates) - l)
            continue

        nodes2 = [n for n in rates if n not in path1]
        for path2 in itertools.permutations(nodes2):
            if j % 100000 == 0:
                print(f"Thread {tid}: ... checked {i}/{n} paths, best so far {M}")

            j += 1

            m1 = part1_calc_given_path(dists, rates, ("AA",) + path1, 26)
            s = sup(rates, path2, 26)
            if M is not None and m1 + s < M:
                i += math.factorial(len(nodes2))
                break

            if length(dists, path2) > 26:
                i += 1
                continue

            i += 1
            m2 = part1_calc_given_path(dists, rates, ("AA",) + path2, 26)
            if M is None or M < m1 + m2:
                M = m1 + m2
                p = (("AA",) + path1, ("AA",) + path2)

    print(f"Thread {tid}: ... checked {i}/{n} paths, best so far {M}")

    return M


def sup(rates: Dict[str, int], path: List[str], time: int) -> int:
    # Best possible outcome of this path if we're allowed to reorder it and assume all nodes are next to each other
    vals = sorted([rates[n] for n in path], reverse=True)
    return sum(r * (time - t) for t, r in enumerate(vals, start=1))


def length(dists: Dict[Tuple[str, str], int], path: List[str]) -> int:
    # Time it takes to travel path and turn on each valve in path
    return sum(dists[(a, b)] for a, b in zip(path, path[1:])) + len(path)


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

    # p1 = part1(copy.deepcopy(data))
    # print(f"Part 1: {p1}")
    N = 7
    M = len([v for v in data.rates.values() if v != 0])

    def f(l):
        return part2_alt_multithread(data, l, l)

    best = None
    with multiprocessing.Pool(processes=N) as pool:
        for m in pool.imap_unordered(f, range(M // 2, 0, -1)):
            if best is None or best < m:
                best = m

            print(f"BEST: {best}")
            with open("best.txt", "w+") as fh:
                print(f"BEST: {best}", file=fh)

    print(f"Part 2: {best}")
