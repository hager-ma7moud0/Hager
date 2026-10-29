"""Make plots and a log-log slope table from results/results.csv.

The slope of log(time) vs log(n) estimates the growth exponent:
  ~1 -> linear / n log n (slightly above 1),  ~2 -> quadratic.
"""
import csv
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CSV = "results/results.csv"
CASES = ["sorted", "reversed", "random"]
STYLE = {
    "insertion": ("tab:red", "o"),
    "merge": ("tab:blue", "s"),
    "quick (last pivot)": ("tab:orange", "^"),
    "quick (random pivot)": ("tab:green", "v"),
    "python sorted()": ("tab:purple", "D"),
}


def load():
    data = {}
    with open(CSV) as f:
        for r in csv.DictReader(f):
            data.setdefault((r["case"], r["algorithm"]), []).append((int(r["n"]), float(r["median_s"])))
    for v in data.values():
        v.sort()
    return data


def slope(points, min_n=2000):
    pts = [(math.log(n), math.log(t)) for n, t in points if n >= min_n and t > 0]
    if len(pts) < 2:
        return float("nan")
    mx = sum(p[0] for p in pts) / len(pts)
    my = sum(p[1] for p in pts) / len(pts)
    return sum((x - mx) * (y - my) for x, y in pts) / sum((x - mx) ** 2 for x, _ in pts)


def main():
    data = load()
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.4), sharey=True)
    for ax, case in zip(axes, CASES):
        for (c, alg), pts in data.items():
            if c != case:
                continue
            color, marker = STYLE[alg]
            ax.plot([p[0] for p in pts], [p[1] for p in pts], marker=marker, color=color, label=alg)
        ax.set_xscale("log"); ax.set_yscale("log")
        ax.set_title(f"{case} input"); ax.set_xlabel("n"); ax.grid(True, which="both", alpha=0.3)
    axes[0].set_ylabel("time (seconds)")
    axes[0].legend(fontsize=8)
    fig.suptitle("Sorting time vs n (log-log; a slope of 1 = linear, 2 = quadratic)")
    fig.tight_layout()
    fig.savefig("results/time_vs_n.png", dpi=160)

    # n log n and n^2 reference comparison for the random case (slide 92: "compare with n log n and n^2")
    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    for alg in ["insertion", "merge", "quick (last pivot)"]:
        pts = data[("random", alg)]
        ns = [p[0] for p in pts]; ts = [p[1] for p in pts]
        color, marker = STYLE[alg]
        ax.plot(ns, ts, marker=marker, color=color, label=alg)
    n0 = 2000
    t_ins = dict(data[("random", "insertion")])[n0]
    t_mrg = dict(data[("random", "merge")])[n0]
    ns = [1000, 2000, 5000, 10000, 20000, 50000, 100000]
    ax.plot([n for n in ns if n <= 10000], [t_ins * (n / n0) ** 2 for n in ns if n <= 10000], "k--", lw=1, label="c * n^2")
    ax.plot(ns, [t_mrg * (n * math.log(n)) / (n0 * math.log(n0)) for n in ns], "k:", lw=1.4, label="c * n log n")
    ax.set_xscale("log"); ax.set_yscale("log"); ax.grid(True, which="both", alpha=0.3)
    ax.set_xlabel("n"); ax.set_ylabel("time (seconds)"); ax.set_title("Random input vs reference curves")
    ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig("results/random_vs_reference.png", dpi=160)

    lines = ["case,algorithm,slope(n>=2000),time_at_largest_n_s,largest_n"]
    for (case, alg), pts in sorted(data.items()):
        lines.append(f"{case},{alg},{slope(pts):.2f},{pts[-1][1]:.4f},{pts[-1][0]}")
    open("results/slopes.csv", "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
