from __future__ import annotations

from typing import Callable


def _to_num(l_bin: list[int]) -> int:
    num = 0
    for idx, el in enumerate(reversed(l_bin)):
        num += (1 if el > 0 else 0) * (2 ** idx)
    return num


def _get_acc(m: list[list[int]]) -> list[int]:
    acc = [0 for i in range(len(m[0]))]

    for row in m:
        for idx, el in enumerate(row):
            acc[idx] += 1 if el else -1

    return acc


def _gamma_eps_rate(acc: list[int]) -> tuple[int, int]:
    gamma = _to_num(acc)

    eps = _to_num(list(map(lambda x: -x, acc)))

    return (gamma, eps)


def _apply_filter(m: list[list[int]], criteria: Callable[[int], int]) -> list[int]:
    idxs = list(range(len(m)))
    for idx in range(len(m[0])):
        new_idxs = []

        el = 0
        for m_idx in idxs:
            el += 1 if m[m_idx][idx] else -1
        el = criteria(el)

        for m_idx in idxs:
            if m[m_idx][idx] == el:
                new_idxs.append(m_idx)
        idxs = new_idxs
        if len(idxs) == 1:
            break
    return m[idxs[0]]


def _o2_co2_rate(m: list[list[int]]) -> tuple[int, int]:
    o2 = _to_num(_apply_filter(m, lambda x: x >= 0))

    co2 = _to_num(_apply_filter(m, lambda x: x < 0))

    return (o2, co2)


def solve(input_text: str) -> tuple[int, int]:

    matrix = list(map(lambda l: list(map(lambda x: int(x), l)), input_text.splitlines()))

    acc = _get_acc(matrix)

    gamma, eps = _gamma_eps_rate(acc)

    o2, co2 = _o2_co2_rate(matrix)

    return (gamma * eps, o2 * co2)
