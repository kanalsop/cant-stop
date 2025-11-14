## Can't Stop Probability Helper

This project explores the dice math behind _Can't Stop_. Each turn in the board game you roll four dice, split them into two pairs however you wish, and advance the corresponding columns. This repository provides tools to inspect the odds of those pair sums and evaluate specific combinations for strategy planning.

### Features

- Enumerate every two-die sum achievable from a four-die roll and print the probability table from 1–12.
- Accept three target sums (between 2 and 12) via CLI arguments and report the probability that any of them appear in a single roll.
- Run `run_all.sh` to calculate the above probability for every unique combination of three sums, great for scouting the most promising columns.
- Visualize the most promising column trios with `analyze_combinations.py`, which prints a ranked table and plots the top results.
- Generate heatmaps and CSV tables for every fixed first column (`x`) using `visualize_slices.py`, saving outputs to `out/imgs/` and `out/tables/`, plus a histogram summarizing the full probability distribution.

### Usage

```bash
# Show the sum table and probability of seeing 5, 7, or 9.
python3 main.py 5 7 9

# Just the probability for the targets (skip the table).
python3 main.py --no-table 4 6 8

# Evaluate every unique 3-sum combination.
./run_all.sh > results.txt

# Rank and plot the best combinations (saved to PNG, skip showing window).
python3 analyze_combinations.py --top 10 --output best_combos.png --no-show

# Create slice heatmaps/tables and the global histogram (saved to out/imgs and out/tables).
python3 visualize_slices.py
```
