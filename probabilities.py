from itertools import product
from typing import Iterable

NUM_DICES = 4
TOTAL_OUTCOMES = 6**NUM_DICES


def _achievable_sums(roll: Iterable[int]) -> set[int]:
    """Return every distinct sum obtainable from any two dice in the roll."""
    roll_list = list(roll)
    sums = set()
    for i in range(NUM_DICES):
        for j in range(i + 1, NUM_DICES):
            sums.add(roll_list[i] + roll_list[j])
    return sums


def sum_probabilities() -> dict[int, float]:
    """Probability distribution for every possible two-die sum."""
    counts = {total: 0 for total in range(1, 13)}
    for roll in product(range(1, 7), repeat=NUM_DICES):
        for total in _achievable_sums(roll):
            counts[total] += 1

    return {total: counts[total] / TOTAL_OUTCOMES for total in counts}


def probability_of_any(target_sums: Iterable[int]) -> float:
    """Probability that at least one of the target sums is achievable."""
    targets = set(target_sums)
    hits = 0
    for roll in product(range(1, 7), repeat=NUM_DICES):
        if _achievable_sums(roll) & targets:
            hits += 1
    return hits / TOTAL_OUTCOMES
