import argparse

from probabilities import probability_of_any, sum_probabilities


def _valid_sum(value: str) -> int:
    try:
        total = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"{value!r} is not a valid integer.") from exc

    if not 2 <= total <= 12:
        raise argparse.ArgumentTypeError(f"{total} must be between 2 and 12.")
    return total


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compute two-dice sum probabilities for Can't Stop "
            "and evaluate three target sums."
        )
    )
    parser.add_argument(
        "numbers",
        metavar="N",
        type=_valid_sum,
        nargs=3,
        help="Three integers between 2 and 12 inclusive.",
    )
    parser.add_argument(
        "--no-table",
        action="store_true",
        help="Skip printing the full sum probability table.",
    )
    return parser.parse_args()


def print_table():
    probabilities = sum_probabilities()
    print("sum probability")
    for total in range(1, 13):
        print(f"{total:>3} {probabilities[total]:.6f}")


def main():
    args = parse_args()
    if not args.no_table:
        print_table()

    targets: list[int] = args.numbers
    probability = probability_of_any(targets)
    formatted_targets = ", ".join(str(n) for n in targets)
    print(
        f"Probability of seeing any of ({formatted_targets}) in one roll: "
        f"{probability:.6f}"
    )


if __name__ == "__main__":
    main()
