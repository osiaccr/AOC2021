from __future__ import annotations

from itertools import chain


def _find_uniques(input_text: str) -> int:
    display_outputs = list(chain(*map(lambda s: s.split("|")[1].split(), input_text.splitlines())))

    return sum(len(s) in [2, 3, 4, 7] for s in display_outputs)


def _parse(input_text: str) -> list[tuple[list[set[str]], list[set[str]]]]:
    def _line_mapper(line: str) -> tuple[list[set[str]], list[set[str]]]:
        signals, output = line.split("|")

        return list(map(frozenset, signals.split())), list(map(frozenset, output.split()))  # type: ignore

    return list(map(_line_mapper, input_text.splitlines()))


def _mapping(signals: list[set[str]]) -> dict[set[str], int]:
    (one,) = [x for x in signals if len(x) == 2]
    (four,) = [x for x in signals if len(x) == 4]
    (seven,) = [x for x in signals if len(x) == 3]
    (eight,) = [x for x in signals if len(x) == 7]

    # 2, 3, 5
    seg_5 = [x for x in signals if len(x) == 5]
    # only 3 contains all segments from 1
    (three,) = [x for x in seg_5 if one <= x]
    # only 5 has the segments of 4 that are not in 1
    (five,) = [x for x in seg_5 if four - one <= x]
    # 2 is the other
    (two,) = [x for x in seg_5 if x is not three and x is not five]

    # 0, 6, 9
    seg_6 = [x for x in signals if len(x) == 6]
    # only 9 contains all segments from 4
    (nine,) = [x for x in seg_6 if four <= x]
    # 0 contains 1 and is not 9
    (zero,) = [x for x in seg_6 if x is not nine and one <= x]
    # 6 is the other
    (six,) = [x for x in seg_6 if x is not nine and x is not zero]

    return {zero: 0, one: 1, two: 2, three: 3, four: 4, five: 5, six: 6, seven: 7, eight: 8, nine: 9}


def _output(signals: list[set[str]], outputs: list[set[str]]) -> int:
    mapping = _mapping(signals)
    res = 0
    for out in outputs:
        res = res * 10 + mapping[out]
    return res


def solve(input_text: str) -> tuple[int, int]:

    count_uniques = _find_uniques(input_text)

    # This somehow ran of the 1st try -- B)
    output_sum = 0
    for signals, outputs in _parse(input_text):
        output_sum += _output(signals, outputs)

    return (count_uniques, output_sum)
