from __future__ import annotations

from collections import Counter
from functools import reduce
from operator import add
from sys import maxsize
from typing import Any, Callable

Graph = dict[str, list[str]]


def _count_paths(graph: Graph, start: str, end: str, visit_limit: Callable[[Counter[str], str], int]) -> int:
    visits: Counter[str] = Counter()

    def _back(node: str) -> int:
        if node == end:
            return 1
        else:
            visits[node] += 1
            paths = reduce(add, [_back(n) for n in graph[node] if visits[n] < visit_limit(visits, n)], 0)
            visits[node] -= 1

            return paths

    return _back(start)


def _unlimited_small_visit_limit(_: Any, node: str) -> int:
    if node.isupper():
        return maxsize  # a pseudo inf
    return 1


def _twice_small_visit_limit(visits: Counter[str], node: str) -> int:
    if node.isupper():
        return maxsize
    elif node in ["start", "end"]:
        return 1
    # No other small cave has been visited twice before
    elif not any(key.islower() and val >= 2 for key, val in visits.items()):
        return 2
    return 1


def _parse(input_text: str) -> Graph:
    edges = [(start, end) for start, end in [line.split("-") for line in input_text.splitlines()]]
    graph: Graph = {}

    for start, end in edges:
        if start not in graph:
            graph[start] = []
        if end not in graph:
            graph[end] = []

        graph[start].append(end)
        graph[end].append(start)

    return graph


def solve(input_text: str) -> tuple[int, int]:
    graph = _parse(input_text)

    paths = _count_paths(graph, "start", "end", _unlimited_small_visit_limit)

    complex_paths = _count_paths(graph, "start", "end", _twice_small_visit_limit)

    return (paths, complex_paths)
