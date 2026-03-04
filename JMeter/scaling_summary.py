import re
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ================= CONFIG =================
HORIZONTAL_DIR = Path("results/horizontal-scaling")
VERTICAL_DIR = Path("results/vertical-scaling")

DELTA = 4
TOTAL_TIME = 5

LANGUAGES = ["python", "java", "js"]

COLORS = {
    "horizontal": "#ff4500",
    "vertical": "#1e90ff"
}

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
    if len(df) == 0:
        return 0
    df = df[df["responseCode"] == 200]
    return len(df) / TOTAL_TIME

def detect_language(name):
    for l in LANGUAGES:
        if name.startswith(l):
            return l.capitalize()
    return None

def detect_architecture(name):
    return "Monolit" if "monolith" in name else "Mikroserwisy gRPC"

# ================= LOAD ALL DATA =================
rows = []

# ---- HORIZONTAL ----
for inst_dir in HORIZONTAL_DIR.iterdir():  # 1-instance / 2-instance / 4-instance
    if not inst_dir.is_dir():
        continue

    replicas = inst_dir.name.split("-")[0]

    for impl_dir in inst_dir.iterdir():
        if not impl_dir.is_dir():
            continue

        lang = detect_language(impl_dir.name)
        if lang is None:
            continue

        arch = detect_architecture(impl_dir.name)

        for iter_dir in impl_dir.iterdir():
            if not iter_dir.is_dir():
                continue

            for csv in iter_dir.glob("users_*.csv"):
                df = pd.read_csv(csv)
                df["timeStamp"] -= df["timeStamp"].min()

                bench = get_benchmark_df(df)
                thr = compute_throughput(bench)

                rows.append({
                    "language": lang,
                    "architecture": arch,
                    "scaling": "horizontal",
                    "scale": replicas,
                    "throughput": thr
                })

# ---- VERTICAL ----
for machine_dir in VERTICAL_DIR.iterdir():  # c2d-standard-*
    if not machine_dir.is_dir():
        continue

    machine = machine_dir.name

    for impl_dir in machine_dir.iterdir():
        if not impl_dir.is_dir():
            continue

        lang = detect_language(impl_dir.name)
        if lang is None:
            continue

        arch = detect_architecture(impl_dir.name)

        for iter_dir in impl_dir.iterdir():
            if not iter_dir.is_dir():
                continue

            for csv in iter_dir.glob("users_*.csv"):
                df = pd.read_csv(csv)
                df["timeStamp"] -= df["timeStamp"].min()

                bench = get_benchmark_df(df)
                thr = compute_throughput(bench)

                rows.append({
                    "language": lang,
                    "architecture": arch,
                    "scaling": "vertical",
                    "scale": machine,
                    "throughput": thr
                })

df = pd.DataFrame(rows)

# ================= MAX THROUGHPUT =================
max_df = (
    df.groupby(["language", "architecture", "scaling", "scale"])
      .max()
      .reset_index()
)

# ================= PLOTS =================
for lang in max_df.language.unique():
    fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=True)
    fig.suptitle(f"Porównanie mechanizmów skalowania dla języka {lang}", fontsize=16)

    for ax, scale in zip(axes, ["2", "4"]):
        h = max_df[(max_df.language == lang) &
                   (max_df.scaling == "horizontal") &
                   (max_df.scale == scale)]

        v = max_df[(max_df.language == lang) &
                   (max_df.scaling == "vertical")]

        labels = ["Mikroserwisy gRPC", "Monolit"]
        x = np.arange(len(labels))
        width = 0.35

        h_vals = [
            h[h.architecture == "Mikroserwisy gRPC"].throughput.values[0],
            h[h.architecture == "Monolit"].throughput.values[0]
        ]

        v_vals = [
            v[v.architecture == "Mikroserwisy gRPC"].throughput.max(),
            v[v.architecture == "Monolit"].throughput.max()
        ]

        ax.bar(x - width/2, h_vals, width, label="Horyzontalne", color=COLORS["horizontal"])
        ax.bar(x + width/2, v_vals, width, label="Wertykalne", color=COLORS["vertical"])

        ax.set_title(f"{scale}× zasoby")
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.set_ylim(bottom=0)
        ax.grid(axis="y", alpha=0.3)

    axes[0].set_ylabel("Przepustowość [req/s]")
    axes[0].legend()
    plt.tight_layout()
    plt.show()

# ================= TABLES =================
def make_table(df, scaling, scale):
    t = df[(df.scaling == scaling) & (df.scale == scale)]
    t = t.sort_values(["language", "architecture"])
    t = t.reset_index(drop=True)
    t.index += 1
    return t[["language", "architecture", "throughput"]]

print("\n=== TABELA: 2 REPLIKI (HORYZONTALNE) ===")
print(make_table(max_df, "horizontal", "2"))

print("\n=== TABELA: 4 REPLIKI (HORYZONTALNE) ===")
print(make_table(max_df, "horizontal", "4"))

print("\n=== TABELA: VERTICAL SCALING (MAX) ===")
print(
    max_df[max_df.scaling == "vertical"]
    .sort_values(["language", "architecture"])
    [["language", "architecture", "scale", "throughput"]]
)
