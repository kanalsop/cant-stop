import argparse
from itertools import combinations
from typing import Iterable, List, Sequence, Tuple

import matplotlib.pyplot as plt

from probabilities import probability_of_any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Evaluate every unique three-column choice (2-12) in Can't Stop "
            "and visualize the best options."
        )
    )
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="Number of highest-probability combinations to display/plot.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Optional path to save the plot as an image.",
    )
    parser.add_argument(
        "--no-show",
        action="store_true",
        help="Skip displaying the plot window (useful for batch runs).",
    )
    return parser.parse_args()


def compute_results() -> List[Tuple[Tuple[int, int, int], float]]:
    combos: Iterable[Tuple[int, int, int]] = combinations(range(2, 13), 3)
    results = []
    for combo in combos:
        prob = probability_of_any(combo)
        results.append((combo, prob))
    results.sort(key=lambda item: item[1], reverse=True)
    return results


def format_combo(combo: Sequence[int]) -> str:
    return "-".join(str(value) for value in combo)


def print_table(results: List[Tuple[Tuple[int, int, int], float]], limit: int) -> None:
    print(f"Top {limit} combinations")
    print("combo probability")
    for combo, probability in results[:limit]:
        print(f"{format_combo(combo):>7} {probability:.6f}")


def plot_top(
    results: List[Tuple[Tuple[int, int, int], float]],
    limit: int,
    output_path: str | None,
    show_plot: bool,
) -> None:
    top = results[:limit]
    labels = [format_combo(combo) for combo, _ in top]
    probabilities = [prob for _, prob in top]

    fig, ax = plt.subplots(figsize=(8, 4 + limit * 0.2))
    ax.barh(labels, probabilities, color="#4B8BBE")
    ax.set_xlabel("Probability")
    ax.set_title(f"Top {limit} Can't Stop column combinations")
    ax.invert_yaxis()
    ax.grid(axis="x", linestyle="--", linewidth=0.5)
    plt.tight_layout()

    if output_path:
        fig.savefig(output_path, dpi=150)
        print(f"Saved plot to {output_path}")
    if show_plot:
        plt.show()
    else:
        plt.close(fig)


def main():
    args = parse_args()
    top_n = max(1, args.top)
    results = compute_results()
    top_n = min(top_n, len(results))
    print_table(results, top_n)
    plot_top(results, top_n, args.output, not args.no_show)


if __name__ == "__main__":
    main()
