from __future__ import annotations

from collections import Counter
from dataclasses import dataclass


def _sign(x: int) -> int:
    if x >= 0:
        return 1
    return -1


@dataclass(frozen=True)
class Point:

    x: int
    y: int


@dataclass(frozen=True)
class Line:

    p1: Point
    p2: Point

    def is_simple(self) -> bool:
        return self.p1.x == self.p2.x or self.p1.y == self.p2.y

    def is_diag(self) -> bool:
        return self.is_simple() or abs(self.p1.x - self.p2.x) == abs(self.p1.y - self.p2.y)

    def get_crossing_points(self) -> list[Point]:
        if self.p1.x == self.p2.x:
            min_y = min(self.p1.y, self.p2.y)
            max_y = max(self.p1.y, self.p2.y)
            return [Point(self.p1.x, y) for y in range(min_y, max_y + 1)]

        if self.p1.y == self.p2.y:
            min_x = min(self.p1.x, self.p2.x)
            max_x = max(self.p1.x, self.p2.x)
            return [Point(x, self.p1.y) for x in range(min_x, max_x + 1)]

        if abs(self.p1.x - self.p2.x) == abs(self.p1.y - self.p2.y):
            vx = _sign(self.p2.x - self.p1.x)
            vy = _sign(self.p2.y - self.p1.y)

            x = self.p1.x
            y = self.p1.y
            points = [Point(x, y)]
            while x != self.p2.x:
                x += vx
                y += vy
                points.append(Point(x, y))

            return points

        raise Exception("Can't handle complex lines")


def _parse(input_text: str) -> list[Line]:
    lines = []
    for input_line in input_text.splitlines():
        l1, l2 = input_line.split(" -> ")
        x1, y1 = l1.split(",")
        x2, y2 = l2.split(",")
        lines.append(Line(Point(int(x1), int(y1)), Point(int(x2), int(y2))))
    return lines


def _multi_crossed(lines: list[Line]) -> int:
    c: Counter[Point] = Counter()
    for line in lines:
        for point in line.get_crossing_points():
            c[point] += 1
    total = 0
    for _, value in c.items():
        if value > 1:
            total += 1
    return total


def solve(input_text: str) -> tuple[int, int]:
    lines = _parse(input_text)

    simple_lines = [line for line in lines if line.is_simple()]

    multi_crossed = _multi_crossed(simple_lines)

    diag_lines = [line for line in lines if line.is_diag()]

    diag_multi_crossed = _multi_crossed(diag_lines)

    return (multi_crossed, diag_multi_crossed)
