from __future__ import annotations

import re


def _hits(velocity: tuple[int, int], target: tuple[int, int, int, int]) -> bool:
    v_x, v_y = velocity
    x_min, x_max, y_min, y_max = target

    x, y = 0, 0

    while x <= x_max and y >= y_min:
        if x in range(x_min, x_max + 1) and y in range(y_min, y_max + 1):
            return True

        x, y = x + v_x, y + v_y
        v_x = v_x - 1 if v_x > 0 else 0
        v_y -= 1

    return False


def _parse(input_text: str) -> tuple[int, int, int, int]:
    x_min, x_max, y_min, y_max = map(int, re.findall(r"-?\d+", input_text))

    if x_min < 0 or x_max < 0:
        raise Exception("Can't handle x coord < 0")

    if y_max > 0:
        raise Exception("Can't handle y coords > 0")

    return x_min, x_max, y_min, y_max


def solve(input_text: str) -> tuple[int, int]:
    """
    This day is quite math heavy and worth and explanation:

    For part 1, highest y, there are somethings to notice:
    1. You can think of x and y axis separetly, they don't interact
    2. For the x axis, you can calculate the min and max velocity with the
        formulas bellow. This is because the projectile will travel (x_v + 1) * x_v // 2
        points before stopping.
        Bonus: it does not matter what v_x you choose for the first part, it just has be
        in that range
    3. For the y, the projectile travel up for (v_y + 1) * v_y // 2 and the returns back.
        When it reaches y=0 (which it allways will because it visits the points going down
        as going up) it will have the velocity if -v_y. The next position after 0 will be
        -v_y.
        The trick is to realise that if -v_y is the first negative position hit, so we want
        it to be at the edge of the taget (y_min) so we set v_y = y_min
    """

    x_min, x_max, y_min, y_max = _parse(input_text)

    # v_x_min = ceil((-1 + sqrt(1 + 8 * x_min)) / 2)
    # v_x_max = floor((-1 + sqrt(1 + 8 * x_max)) / 2)

    highest_y = (y_min + 1) * y_min // 2

    total_hits = 0
    for v_x in range(300):
        for v_y in range(-300, 300):
            total_hits += _hits((v_x, v_y), (x_min, x_max, y_min, y_max))

    return highest_y, total_hits
