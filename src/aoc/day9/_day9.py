from __future__ import annotations
from functools import reduce

from operator import add


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


def _lowpoints(floor: list[list[int]]) -> list[tuple[int, int]]:
    n = len(floor)
    m = len(floor[0])

    low_points: list[tuple[int, int]] = []

    for x in range(0, n):
        for y in range(0, m):
            val = floor[x][y]
            nbhs = _neighbours((x, y), (n, m))
            if all(floor[n_x][n_y] > val for n_x, n_y in nbhs):
                low_points.append((x, y))

    return low_points


def _fill(floor: list[list[int]], p: tuple[int, int]) -> list[tuple[int, int]]:

    size = (len(floor), len(floor[0]))

    basin: list[tuple[int, int]] = []

    def _back(_p: tuple[int, int]) -> None:
        basin.append(_p)
        for nbh in [n for n in _neighbours(_p, size) if floor[n[0]][n[1]] != 9]:
            if nbh not in basin:
                _back(nbh)

    _back(p)

    return basin


def _parse(input_text: str) -> list[list[int]]:
    return list(map(lambda l: list(map(int, l)), input_text.splitlines()))


def solve(input_text: str) -> tuple[int, int]:

    floor = _parse(input_text)

    lowpoints = _lowpoints(floor)

    risk_level = reduce(add, [floor[x][y] + 1 for x, y in lowpoints])

    basins = [_fill(floor, p) for p in lowpoints]

    print(f"{basins=}")

    basin_sizes = sorted(len(b) for b in basins)

    return (risk_level, basin_sizes[-1] * basin_sizes[-2] * basin_sizes[-3])
