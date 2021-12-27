from __future__ import annotations

from collections import Counter
from decimal import InvalidOperation
from statistics import mean, median_high


def _fuel(input_nums: list[int], median: int) -> int:
    fuel = 0
    for x in input_nums:
        fuel += abs(median - x)
    return fuel


def _complex_fuel(input_nums: list[int], median: int) -> int:
    fuel = 0
    for x in input_nums:
        dist = abs(median - x)
        fuel += dist * (dist + 1) // 2
    return fuel


def solve(input_text: str) -> tuple[int, int]:

    input_nums = list(map(int, input_text.split(",")))

    med = median_high(input_nums)
    s_fuel = _fuel(input_nums, med)

    avg = round(mean(input_nums))
    delta = 10
    c_fuel = min(map(lambda x: _complex_fuel(input_nums, x), range(avg - delta, avg + delta)))

    return (s_fuel, c_fuel)
