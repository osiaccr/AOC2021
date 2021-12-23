from __future__ import annotations

from dataclasses import dataclass


def _check_bingo(squares: list[list[Square]]) -> bool:
    for row in squares:
        bingo = True
        for square in row:
            if not square.marked:
                bingo = False
                break
        if bingo:
            return True

    for col_id in range(len(squares[0])):
        bingo = True
        for row_id in range(len(squares)):
            if not squares[row_id][col_id].marked:
                bingo = False
                break
        if bingo:
            return True

    return False


@dataclass
class Square:

    value: int
    marked = False


class Board:
    def __init__(self, items: list[list[int]]) -> None:
        self._squares = list(map(lambda l: list(map(lambda x: Square(x), l)), items))

    def add_value(self, value: int) -> bool:
        for row in self._squares:
            for square in row:
                if square.value == value:
                    square.marked = True

        return _check_bingo(self._squares)

    def get_unmarked_sum(self) -> int:
        sum = 0
        for row in self._squares:
            for square in row:
                if not square.marked:
                    sum += square.value
        return sum


def _parse_text(input_text: str) -> tuple[list[int], list[list[list[int]]]]:
    chunks = input_text.split("\n\n")

    values = list(map(lambda x: int(x), chunks[0].split(",")))
    boards = [
        list(map(lambda l: list(map(lambda x: int(x), l.split())), board_text.splitlines()))
        for board_text in chunks[1:]
    ]

    return (values, boards)


def _first_bingo(values: list[int], boards: list[Board]) -> int:
    for value in values:
        for board in boards:
            if board.add_value(value):
                return board.get_unmarked_sum() * value

    return 0


def _last_bingo(values: list[int], boards: list[Board]) -> int:
    solutions: list[tuple[Board, int]] = []
    for value in values:
        new_boards: list[Board] = []
        for board in boards:
            if board.add_value(value):
                solutions.append((board, value))
            else:
                new_boards.append(board)
        boards = new_boards
        if not boards:
            break

    last_board, last_value = solutions[-1]
    return last_board.get_unmarked_sum() * last_value


def solve(input_text: str) -> tuple[int, int]:

    values, raw_boards = _parse_text(input_text)

    p1 = _first_bingo(values, [Board(items) for items in raw_boards])

    p2 = _last_bingo(values, [Board(items) for items in raw_boards])

    return (p1, p2)
