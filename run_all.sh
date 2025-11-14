#!/usr/bin/env bash
set -euo pipefail

cd /Users/kanaemon-posl/projects/others/cant-stop

# Run main.py for every unique 3-number combination between 2 and 12.
for ((a = 2; a <= 10; a++)); do
  for ((b = a + 1; b <= 11; b++)); do
    for ((c = b + 1; c <= 12; c++)); do
      uv run main.py --no-table "$a" "$b" "$c"
    done
  done
done
