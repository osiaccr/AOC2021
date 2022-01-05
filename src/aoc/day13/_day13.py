from __future__ import annotations

from itertools import chain
from typing import TypeVar

T = TypeVar("T")


def _paper_to_string(paper: list[list[T]]) -> str:
    return "\n".join("".join("█" if x else " " for x in row) for row in paper)


def _transpose(paper: list[list[T]]) -> list[list[T]]:
    return [list(ll) for ll in [*zip(*paper)]]


def _fold(paper: list[list[bool]], direction: str, coord: int) -> list[list[bool]]:
    def _combine_line(line: list[bool]) -> list[bool]:
        left, right = line[:coord], line[coord + 1 :]
        return [x or y for x, y in zip(left, reversed(right))]

    if direction == "y":
        paper = _transpose(paper)

    paper = [_combine_line(line) for line in paper]

    if direction == "y":
        paper = _transpose(paper)

    return paper


def _parse(input_text: str) -> tuple[list[tuple[int, int]], list[tuple[str, int]]]:
    points_text, folds_text = input_text.split("\n\n")

    # The flip here is intentional, AOC uses X as up-down, I find it confusing
    points = [(int(y), int(x)) for x, y in [s.split(",") for s in points_text.splitlines()]]

    folds = [(direction, int(coord)) for direction, coord in [line[11:].split("=") for line in folds_text.splitlines()]]

    return (points, folds)


def solve(input_text: str) -> tuple[int, int]:

    points, folds = _parse(input_text)

    n, m = max(x for x, _ in points) + 1, max(y for _, y in points) + 1

    paper = [[False for _ in range(m)] for _ in range(n)]
    for x, y in points:
        paper[x][y] = True

    first_fold = _fold(paper, folds[0][0], folds[0][1])

    first_fold_dots = sum(chain.from_iterable(first_fold))

    for direction, coord in folds:
        paper = _fold(paper, direction, coord)

    # Normally solutions to problems are ints, but in this case is a str
    return (first_fold_dots, "\n" + _paper_to_string(paper))  # type: ignore
