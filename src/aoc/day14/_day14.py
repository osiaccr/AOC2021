from __future__ import annotations

from collections import Counter


def _step(polymer: Counter[str], insertions: dict[str, str]) -> Counter[str]:
    n_dist: Counter[str] = Counter()
    for pair, count in polymer.items():
        l_pair, r_pair = pair[0] + insertions[pair], insertions[pair] + pair[1]
        n_dist[l_pair] += count
        n_dist[r_pair] += count
    return n_dist


def _best_worst_delta(polymer: Counter[str], start: str, end: str) -> int:
    chars: Counter[str] = Counter()
    for pair, count in polymer.items():
        chars[pair[0]] += count
        chars[pair[1]] += count
    chars[start] += 1
    chars[end] += 1
    commons = chars.most_common()
    return (commons[0][1] - commons[-1][1]) // 2


def _parse(input_text: str) -> tuple[Counter[str], dict[str, str], tuple[str, str]]:
    polymer, insertions_text = input_text.split("\n\n")
    polymer_dist = Counter(s1 + s2 for s1, s2 in zip(polymer[:-1], polymer[1:]))
    insertions = {pair: insert for pair, insert in [line.split(" -> ") for line in insertions_text.splitlines()]}
    return polymer_dist, insertions, (polymer[0], polymer[-1])


def solve(input_text: str) -> tuple[int, int]:

    polymer, insertions, (start, end) = _parse(input_text)

    n_pol = polymer
    for _ in range(10):
        n_pol = _step(n_pol, insertions)

    delta_10 = _best_worst_delta(n_pol, start, end)

    for _ in range(30):
        n_pol = _step(n_pol, insertions)

    delta_40 = _best_worst_delta(n_pol, start, end)

    return (delta_10, delta_40)
