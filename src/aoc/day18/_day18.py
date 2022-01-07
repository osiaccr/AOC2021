from __future__ import annotations

from dataclasses import astuple, dataclass
from itertools import combinations
from math import ceil
from typing import Iterator, cast


@dataclass(frozen=True)
class Pair:

    left: Pair | int
    right: Pair | int

    def __iter__(self) -> Iterator[Pair | int]:
        return iter(astuple(self))

    def __str__(self) -> str:
        return f"[{self.left},{self.right}]"

    def __add__(self, other: Pair) -> Pair:
        return _reduce(Pair(self, other))


def _explode(pair: Pair) -> Pair:
    def _add_leftmost(pair: Pair | int, val: int) -> Pair | int:
        if isinstance(pair, int):
            return pair + val
        if isinstance(pair.left, int):
            return Pair(pair.left + val, pair.right)
        else:
            return Pair(_add_leftmost(pair.left, val), pair.right)

    def _add_rightmost(pair: Pair | int, val: int) -> Pair | int:
        if isinstance(pair, int):
            return pair + val
        if isinstance(pair.right, int):
            return Pair(pair.left, pair.right + val)
        else:
            return Pair(pair.left, _add_rightmost(pair.right, val))

    def _explode_inner(pair: Pair | int, level: int) -> tuple[Pair | int, tuple[int, int]]:
        if isinstance(pair, int):
            return pair, (0, 0)

        if level == 4:
            return 0, (cast(int, pair.left), cast(int, pair.right))

        e_left, (t_left, t_right) = _explode_inner(pair.left, level + 1)
        if e_left != pair.left:
            return Pair(e_left, _add_leftmost(pair.right, t_right)), (t_left, 0)

        e_right, (t_left, t_right) = _explode_inner(pair.right, level + 1)
        if e_right != pair.right:
            return Pair(_add_rightmost(pair.left, t_left), e_right), (0, t_right)

        return pair, (0, 0)

    e_pair, _ = _explode_inner(pair, 0)
    return cast(Pair, e_pair)


def _split(pair: Pair) -> Pair:
    def _split_inner(pair: Pair | int) -> Pair | int:
        if isinstance(pair, int):
            if pair >= 10:
                return Pair(pair // 2, ceil(pair / 2))
            else:
                return pair

        s_left = _split_inner(pair.left)
        if s_left != pair.left:
            return Pair(s_left, pair.right)

        s_right = _split_inner(pair.right)
        if s_right != pair.right:
            return Pair(pair.left, s_right)

        return pair

    return cast(Pair, _split_inner(pair))


def _reduce(pair: Pair) -> Pair:
    while True:
        e_pair = _explode(pair)
        if e_pair != pair:
            pair = e_pair
            continue

        s_pair = _split(pair)
        if s_pair != pair:
            pair = s_pair
            continue

        return pair


def _magnitude(pair: Pair | int) -> int:
    if isinstance(pair, int):
        return pair
    return 3 * _magnitude(pair.left) + 2 * _magnitude(pair.right)


def _parse(input_text: str) -> list[Pair]:
    def _parse_pair(text: str) -> tuple[Pair | int, str]:
        if text[0] in map(str, range(10)):
            return int(text[0]), text[1:]
        else:
            left, text = _parse_pair(text[1:])  # skip [
            right, text = _parse_pair(text[1:])  # skip ,
            return Pair(left, right), text[1:]  # skip ]

    pairs = [_parse_pair(s)[0] for s in input_text.splitlines()]

    for pair in pairs:
        if isinstance(pair, int):
            raise Exception("An int isn't a valid top-level pair")

    return cast(list[Pair], pairs)


def solve(input_text: str) -> tuple[int, int]:

    pairs = _parse(input_text)

    acc = pairs[0]
    for pair in pairs[1:]:
        n_acc = acc + pair
        # print(f"  {acc}\n+ {pair}\n= {n_acc}\n")
        acc = n_acc

    magnitude = _magnitude(acc)

    couples = combinations(pairs, 2)
    max_mag = max(max(_magnitude(p_1 + p_2), _magnitude(p_2 + p_1)) for p_1, p_2 in couples)

    return magnitude, max_mag
