from __future__ import annotations

import importlib
from typing import TextIO

import click


@click.command()
@click.argument("day", type=int)
@click.argument("input_file", type=click.File())
def _main(day: int, input_file: TextIO) -> None:
    _solver = importlib.import_module(f"aoc.day{day}")
    input_text = input_file.read()
    _p1, _p2 = _solver.solve(input_text)  # type: ignore

    print(f"Solution for day {day}: part 1 = {_p1}, part2 = {_p2}")


if __name__ == "__main__":
    _main()
