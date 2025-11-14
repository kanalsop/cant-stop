import argparse
import csv
from itertools import combinations
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

import matplotlib.pyplot as plt
import numpy as np

from probabilities import probability_of_any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Produce probability tables and heatmaps for each Can't Stop column slice."
        )
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("out"),
        help="Base directory for generated tables and images (default: ./out).",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Display plots interactively in addition to saving them.",
    )
    return parser.parse_args()


def all_combinations() -> Dict[Tuple[int, int, int], float]:
    combos: Iterable[Tuple[int, int, int]] = combinations(range(2, 13), 3)
    return {combo: probability_of_any(combo) for combo in combos}


def ensure_dirs(base: Path) -> Tuple[Path, Path]:
    img_dir = base / "imgs"
    table_dir = base / "tables"
    img_dir.mkdir(parents=True, exist_ok=True)
    table_dir.mkdir(parents=True, exist_ok=True)
    return img_dir, table_dir


def build_grid(
    x: int, combo_map: Dict[Tuple[int, int, int], float]
) -> Tuple[List[int], List[int], np.ndarray, List[Tuple[int, int, int, float]]]:
    y_values = list(range(x + 1, 12))
    z_values = list(range(x + 2, 13))
    grid = np.full((len(y_values), len(z_values)), np.nan, dtype=float)
    rows: List[Tuple[int, int, int, float]] = []

    for yi, y in enumerate(y_values):
        for zi, z in enumerate(z_values):
            if z <= y:
                continue
            probability = combo_map[(x, y, z)]
            grid[yi, zi] = probability
            rows.append((x, y, z, probability))

    return y_values, z_values, grid, rows


def save_table(path: Path, rows: Sequence[Tuple[int, int, int, float]]) -> None:
    with path.open("w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["x", "y", "z", "probability"])
        for x, y, z, probability in rows:
            writer.writerow([x, y, z, f"{probability:.6f}"])


def plot_heatmap(
    x: int,
    y_values: Sequence[int],
    z_values: Sequence[int],
    grid: np.ndarray,
    output_path: Path,
    show_plot: bool,
) -> None:
    masked = np.ma.masked_invalid(grid)
    fig, ax = plt.subplots(figsize=(10, 6))
    im = ax.imshow(
        masked,
        origin="lower",
        cmap="viridis",
        vmin=np.nanmin(grid),
        vmax=np.nanmax(grid),
        aspect="auto",
    )
    ax.set_xticks(range(len(z_values)))
    ax.set_xticklabels(z_values)
    ax.set_yticks(range(len(y_values)))
    ax.set_yticklabels(y_values)
    ax.set_xlabel("z value")
    ax.set_ylabel("y value")
    ax.set_title(f"Probability heatmap for combinations ({x}, y, z)")
    fig.colorbar(im, ax=ax, label="Probability")
    plt.tight_layout()
    fig.savefig(output_path, dpi=150)
    if show_plot:
        plt.show()
    else:
        plt.close(fig)


def plot_distribution(
    probabilities: Sequence[float], output_path: Path, show_plot: bool
) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(probabilities, bins=20, color="#ff9671", edgecolor="black")
    ax.set_xlabel("Probability")
    ax.set_ylabel("Number of (x, y, z) combinations")
    ax.set_title("Distribution of probabilities across all column combinations")
    plt.tight_layout()
    fig.savefig(output_path, dpi=150)
    if show_plot:
        plt.show()
    else:
        plt.close(fig)


def main():
    args = parse_args()
    show_plots = args.show
    img_dir, table_dir = ensure_dirs(args.output_dir)
    combo_map = all_combinations()

    for x in range(2, 11):
        y_vals, z_vals, grid, rows = build_grid(x, combo_map)
        table_path = table_dir / f"slice_x_{x}.csv"
        img_path = img_dir / f"slice_x_{x}.png"
        save_table(table_path, rows)
        plot_heatmap(x, y_vals, z_vals, grid, img_path, show_plots)
        print(f"Saved table to {table_path} and heatmap to {img_path}")

    distribution_path = img_dir / "probability_distribution.png"
    plot_distribution(list(combo_map.values()), distribution_path, show_plots)
    print(f"Saved probability distribution histogram to {distribution_path}")


if __name__ == "__main__":
    main()
