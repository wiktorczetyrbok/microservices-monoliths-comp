import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ======================
# CONFIG
# ======================
BASE_DIR = Path("csv")
OUTPUT_DIR = Path("plots")
OUTPUT_DIR.mkdir(exist_ok=True)

DELTA_SEC = 4
TOTAL_TIME_SEC = 5
MAX_LATENCY = 200

# ======================
# HELPERS
# ======================
def get_benchmark_df(df, delta, total_time):
    df = df.copy()
    df["response_end"] = df["timeStamp"] + df["elapsed"]

    estimated_start = df["timeStamp"].min() + delta * 1000
    benchmark_start = df[df["response_end"] > estimated_start]["response_end"].min()
    benchmark_end = benchmark_start + total_time * 1000

    return df[
        (df["response_end"] >= benchmark_start) &
        (df["response_end"] <= benchmark_end)
        ]


def compute_stats(df, total_time):
    all_requests = len(df)

    df = df[df["responseCode"] == 200]
    successful = len(df)

    error_rate = (all_requests - successful) / all_requests if all_requests else 0
    median_latency = df["Latency"].median()
    q90_latency = df["Latency"].quantile(0.9)

    df = df[df["Latency"] <= MAX_LATENCY]
    throughput = len(df) / total_time

    return throughput, median_latency, q90_latency, error_rate


def extract_users(filename):
    return int(re.search(r"users_(\d+)", filename).group(1))


# ======================
# LOAD DATA
# ======================
records = []

for impl_dir in BASE_DIR.iterdir():
    if not impl_dir.is_dir():
        continue

    for iteration_dir in impl_dir.iterdir():
        if not iteration_dir.is_dir():
            continue

        for csv_file in iteration_dir.glob("users_*.csv"):
            df = pd.read_csv(csv_file)

            df["timeStamp"] -= df["timeStamp"].min()
            bench = get_benchmark_df(df, DELTA_SEC, TOTAL_TIME_SEC)

            throughput, med, q90, err = compute_stats(bench, TOTAL_TIME_SEC)

            records.append({
                "implementation": impl_dir.name,
                "iteration": iteration_dir.name,
                "users": extract_users(csv_file.name),
                "throughput": throughput,
                "median_latency": med,
                "q90_latency": q90,
                "error_rate": err
            })

data = pd.DataFrame(records)

# ======================
# AGGREGATION
# ======================
agg = (
    data
    .groupby(["implementation", "users"])
    .median(numeric_only=True)
    .reset_index()
)

# ======================
# PLOT: THROUGHPUT
# ======================
plt.figure(figsize=(12, 7))

for impl, df_impl in agg.groupby("implementation"):
    df_impl = df_impl.sort_values("users")
    plt.plot(
        df_impl["users"],
        df_impl["throughput"],
        marker="o",
        label=impl
    )

plt.xlabel("Liczba użytkowników")
plt.ylabel("Przepustowość (req/s)")
plt.title("Skalowanie – przepustowość")
plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "throughput_scaling.png", dpi=300)
plt.close()

# ======================
# PLOT: LATENCY
# ======================
plt.figure(figsize=(12, 7))

for impl, df_impl in agg.groupby("implementation"):
    df_impl = df_impl.sort_values("users")
    plt.plot(
        df_impl["users"],
        df_impl["median_latency"],
        marker="o",
        label=impl
    )

plt.xlabel("Liczba użytkowników")
plt.ylabel("Mediana latencji [ms]")
plt.title("Skalowanie – latencja")
plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "latency_scaling.png", dpi=300)
plt.close()

print("✅ Wykresy zapisane w katalogu plots/")
