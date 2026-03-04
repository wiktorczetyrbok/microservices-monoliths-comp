import re
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ================= CONFIG =================
BASE_DIR = Path("csv")
OUT_DIR = Path("plots_svg")
OUT_DIR.mkdir(exist_ok=True)

DELTA = 4
TOTAL_TIME = 5
MAX_LATENCY = 200

COLORS = [
    "#386cb0",  # blue
    "#fdb462",  # orange
    "#7fc97f",  # green
    "#ef3b2c",
    "#662506"
]

# ================= HELPERS =================
def extract_users(fname):
    return int(re.search(r"users_(\d+)", fname).group(1))

def get_benchmark_df(df):
    df = df.copy()
    df["response_end"] = df["timeStamp"] + df["elapsed"]
    start_est = df["timeStamp"].min() + DELTA * 1000
    start = df[df["response_end"] > start_est]["response_end"].min()
    end = start + TOTAL_TIME * 1000
    return df[(df["response_end"] >= start) & (df["response_end"] <= end)]

def compute_throughput(df):
    all_req = len(df)
    df = df[df["responseCode"] == 200]
    df = df[df["Latency"] <= MAX_LATENCY]
    return len(df) / TOTAL_TIME if all_req else 0

# ================= LOAD DATA =================
rows = []

for impl in BASE_DIR.iterdir():
    if not impl.is_dir():
        continue

    for iteration in impl.iterdir():
        if not iteration.is_dir():
            continue

        for csv in iteration.glob("users_*.csv"):
            df = pd.read_csv(csv)
            df["timeStamp"] -= df["timeStamp"].min()

            bench = get_benchmark_df(df)
            thr = compute_throughput(bench)

            rows.append({
                "implementation": impl.name,
                "users": extract_users(csv.name),
                "throughput": thr
            })

df = pd.DataFrame(rows)

# ================= AGGREGATION =================
agg = (
    df.groupby(["implementation", "users"])
      .median()
      .reset_index()
)

# ================= CUT AFTER 90% DROP =================
def trim_after_drop(group):
    group = group.sort_values("users")
    max_thr = group["throughput"].max()
    max_idx = group["throughput"].idxmax()

    after_max = group.loc[group.index > max_idx]
    drop = after_max[after_max["throughput"] < 0.9 * max_thr]

    if len(drop) > 0:
        cut_idx = drop.index[0]
        return group.loc[group.index <= cut_idx]
    return group

trimmed = (
    agg.groupby("implementation", group_keys=False)
       .apply(trim_after_drop)
)

# ================= PLOTTING =================
plt.rcParams.update({
    "font.size": 12,
    "axes.edgecolor": "black",
    "axes.linewidth": 1,
})

for impl, data in trimmed.groupby("implementation"):
    data = data.sort_values("users")
    color = COLORS[hash(impl) % len(COLORS)]

    plt.figure(figsize=(8, 5))
    plt.plot(
        data["users"],
        data["throughput"],
        marker="o",
        linewidth=2,
        color=color
    )

    # mark max
    idx = data["throughput"].idxmax()
    x = data.loc[idx, "users"]
    y = data.loc[idx, "throughput"]

    plt.scatter(x, y, color="black", marker="^", s=80, zorder=5)
    plt.text(x, y * 1.02, f"{y:.1f}", ha="center", fontsize=11)

    plt.title(impl)
    plt.xlabel("Liczba użytkowników")
    plt.ylabel("Przepustowość [req/s]")
    plt.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUT_DIR / f"{impl}_vertical_scaling.svg", format="svg")
    plt.close()

print("✅ SVG zapisane w plots_svg/")
