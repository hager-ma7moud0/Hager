"""Benchmark: time each sorting algorithm on sorted / reversed / random data.

Usage:  python benchmark.py            (full run, writes results/results.csv)
        python benchmark.py --quick    (small sizes, ~seconds, for a sanity check)
"""
import argparse
import csv
import gc
import os
import random
import statistics
import time

from sorts import ALGORITHMS

SIZES = [1_000, 2_000, 5_000, 10_000, 20_000, 50_000, 100_000]
QUICK_SIZES = [500, 1_000, 2_000]
CASES = ["sorted", "reversed", "random"]

# Python is ~100x slower than C, so algorithms that are Theta(n^2) on a given input
# are only run up to this size (otherwise n = 100,000 would take hours).
QUADRATIC_LIMIT = 10_000
QUADRATIC = {
    ("insertion", "reversed"), ("insertion", "random"),
    ("quick (last pivot)", "sorted"), ("quick (last pivot)", "reversed"),
}

SEED = 314


def make_data(case, n, rng):
    if case == "sorted":
        return list(range(n))
    if case == "reversed":
        return list(range(n, 0, -1))
    return [rng.randint(0, 10 * n) for _ in range(n)]


def repeats_for(n):
    return 5 if n <= 2_000 else 3 if n <= 20_000 else 2


def time_once(fn, data):
    gc.collect()
    t0 = time.perf_counter()
    fn(data)
    return time.perf_counter() - t0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--out", default="results/results.csv")
    args = ap.parse_args()
    sizes = QUICK_SIZES if args.quick else SIZES
    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    rows = []
    for case in CASES:
        for n in sizes:
            rng = random.Random(SEED + n)
            data = make_data(case, n, rng)
            for name, fn in ALGORITHMS.items():
                if (name, case) in QUADRATIC and n > QUADRATIC_LIMIT:
                    continue
                times = [time_once(fn, data) for _ in range(repeats_for(n))]
                rows.append({
                    "case": case, "n": n, "algorithm": name,
                    "median_s": statistics.median(times), "min_s": min(times),
                    "repeats": len(times),
                })
                print(f"{case:9s} n={n:>7,d} {name:22s} {statistics.median(times):10.4f}s", flush=True)

    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    print("saved", args.out)


if __name__ == "__main__":
    main()
