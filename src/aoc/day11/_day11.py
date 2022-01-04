from __future__ import annotations

from itertools import count
from typing import cast


def _neighbours(p: tuple[int, int], size: tuple[int, int]) -> list[tuple[int, int]]:
    delta_x = [1, -1, 0, 0, 1, 1, -1, -1]
    delta_y = [0, 0, 1, -1, -1, 1, -1, 1]

    p_x, p_y = p
    n, m = size

    nps: list[tuple[int, int]] = []

    for d_x, d_y in zip(delta_x, delta_y):
        n_x, n_y = p_x + d_x, p_y + d_y
        if n_x in range(0, n) and n_y in range(0, m):
            nps.append((n_x, n_y))

    return nps


def _step(table: list[list[int]]) -> tuple[list[list[int]], int]:
    n, m = len(table), len(table[0])
    n_table: list[list[int | None]] = [[x + 1 for x in row] for row in table]

    def _flash() -> bool:
        for x in range(n):
            for y in range(m):
                val = n_table[x][y]
                if val is not None and val >= 10:
                    for n_x, n_y in [
                        (n_x, n_y) for n_x, n_y in _neighbours((x, y), (n, m)) if n_table[n_x][n_y] is not None
                    ]:
                        # mypy is not smart enough to pick up that n_table[n_x][n_y] is not None
                        n_table[n_x][n_y] += 1  # type: ignore
                    n_table[x][y] = None
                    return True
        return False

    flashes = 0
    while _flash():
        flashes += 1

    return ([[0 if x is None else x for x in row] for row in n_table], flashes)


def _run_steps(table: list[list[int]], step_count: int) -> int:
    flashes = 0
    for _ in range(step_count):
        table, n_flashes = _step(table)
        print(f"{table=}")
        flashes += n_flashes
    return flashes


def _find_sync(table: list[list[int]]) -> int | None:
    for idx in count(start=1):
        table, _ = _step(table)
        if all(all(x == 0 for x in row) for row in table):
            return idx
    return None


def _parse(input_text: str) -> list[list[int]]:
    return list(map(lambda l: list(map(int, l)), input_text.splitlines()))


def solve(input_text: str) -> tuple[int, int]:
    table = _parse(input_text)

    flashes = _run_steps(table, 100)

    # _find_sync never really returns None, it either returns an int or never halts, which mypy can't model
    sync = cast(int, _find_sync(table))

    return (flashes, sync)
