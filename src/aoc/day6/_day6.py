from __future__ import annotations

from collections import Counter

MAX_DAYS = 8


def _next_state(state: Counter[int]) -> Counter[int]:
    new_state: Counter[int] = Counter()

    for idx in range(MAX_DAYS):
        new_state[idx] = state[idx + 1]

    new_state[6] += state[0]
    new_state[8] += state[0]

    return new_state


def _evolve(initial_state: Counter[int], days: int) -> Counter[int]:
    for _ in range(days):
        initial_state = _next_state(initial_state)
    return initial_state


def _parse(input_text: str) -> list[int]:
    return list(map(lambda x: int(x), input_text.strip().split(",")))


def solve(input_text: str) -> tuple[int, int]:

    input_nums = _parse(input_text)

    initial_state = Counter(input_nums)

    after_80_state = _evolve(initial_state, 80)
    after_80 = sum(after_80_state.values())

    after_256_state = _evolve(after_80_state, 256 - 80)
    after_256 = sum(after_256_state.values())

    return (after_80, after_256)
