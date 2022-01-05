from __future__ import annotations

from queue import PriorityQueue
from sys import maxsize
from typing import Generator, cast

import numpy as np


def _neighbours(p: tuple[int, int], size: tuple[int, int]) -> list[tuple[int, int]]:
    delta_x = [1, -1, 0, 0]
    delta_y = [0, 0, 1, -1]

    p_x, p_y = p
    n, m = size

    nps: list[tuple[int, int]] = []

    for d_x, d_y in zip(delta_x, delta_y):
        n_x, n_y = p_x + d_x, p_y + d_y
        if n_x in range(0, n) and n_y in range(0, m):
            nps.append((n_x, n_y))

    return nps


def _min_cost_path(map: list[list[int]]) -> int:
    n, m = len(map), len(map[0])

    disk = [[maxsize for _ in range(m)] for _ in range(n)]
    pq: PriorityQueue[tuple[int, tuple[int, int]]] = PriorityQueue()

    pq.put_nowait((0, (0, 0)))
    disk[0][0] = 0

    while not pq.empty():
        _, (x, y) = pq.get_nowait()

        for (n_x, n_y) in _neighbours((x, y), (n, m)):
            n_cost = map[n_x][n_y]
            if disk[n_x][n_y] > disk[x][y] + n_cost:
                disk[n_x][n_y] = disk[x][y] + n_cost
                pq.put_nowait((disk[n_x][n_y], (n_x, n_y)))

    return disk[n - 1][m - 1]


def _expand(map: list[list[int]]) -> list[list[int]]:
    def _map_cycler(map: list[list[int]], take: int) -> Generator[list[list[int]], None, None]:
        for _ in range(take):
            yield map
            map = [[x + 1 if x <= 8 else 1 for x in row] for row in map]

    matricies = [[np.array(matrix) for matrix in _map_cycler(row_seed, 5)] for row_seed in _map_cycler(map, 5)]

    return cast(list[list[int]], np.concatenate([np.concatenate(row, axis=1) for row in matricies], axis=0).tolist())


def _parse(input_text: str) -> list[list[int]]:
    return list(map(lambda l: list(map(int, l)), input_text.splitlines()))


def solve(input_text: str) -> tuple[int, int]:

    map = _parse(input_text)

    min_cost_path = _min_cost_path(map)

    expanded_map = _expand(map)

    expanded_min = _min_cost_path(expanded_map)

    return min_cost_path, expanded_min


"""
I misunderstood how to do the expansion, this expands each value in the original map to something like this:

8 9 1 2 3
9 1 2 3 4
1 2 3 4 5
2 3 4 5 6
3 4 5 6 7

Where the top left is the seed and all other increase with 1 wrapping at 10.

I spent too much time on this to delete it!

def _crange(begin: int, end: int, start: int | None = None, step: int = 1, take: int | None = None) -> Generator[int]:
    taken = 0
    x = start if start is not None and start < end else begin
    while True:
        yield x
        taken += 1
        if take is not None and taken >= take:
            break
        x = x + step if x + step < end else begin


def _expand(map: list[list[int]]) -> list[list[int]]:
    matricies = [
        [
            np.array(
                [[_y for _y in _crange(1, 10, start=_x, take=5)] for _x in _crange(1, 10, start=x, take=5)]
            ).reshape(5, 5)
            for x in row
        ]
        for row in map
    ]
    return np.concatenate([np.concatenate(row, axis=1) for row in matricies], axis=0).tolist()
"""
