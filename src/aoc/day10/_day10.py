from __future__ import annotations

from functools import reduce
from operator import add
from statistics import median_high


def _autocomplete(line: str) -> tuple[int, str] | list[str]:
    stack: list[str] = []

    inverse = {"(": ")", "[": "]", "{": "}", "<": ">", ")": "(", "]": "[", "}": "{", ">": "<"}

    for idx, p in enumerate(line):
        if p in "([{<":
            stack.append(p)
        elif stack[-1] != inverse[p]:
            return (idx, p)
        else:
            stack.pop()

    return [inverse[s] for s in reversed(stack)]


def _complete_score(line: list[str]) -> int:
    complete_value = {")": 1, "]": 2, "}": 3, ">": 4}

    return reduce(lambda x, y: x * 5 + y, [complete_value[c] for c in line], 0)


def solve(input_text: str) -> tuple[int, int]:

    autocomplete = [_autocomplete(l) for l in input_text.splitlines()]

    error_value = {")": 3, "]": 57, "}": 1197, ">": 25137}

    syntax_error_score = reduce(add, [error_value[t[1]] for t in autocomplete if isinstance(t, tuple)])

    complete_score = median_high(_complete_score(l) for l in autocomplete if isinstance(l, list))

    return (syntax_error_score, complete_score)
