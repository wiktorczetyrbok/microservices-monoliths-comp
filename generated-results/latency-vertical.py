import re
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# ================= CONFIG =================
BASE_DIR = Path("results/vertical-scaling")
OUT_DIR = Path("plots-images/vertical-scaling")
OUT_DIR.mkdir(parents=True, exist_ok=True)

DELTA = 4
TOTAL_TIME = 5

COLORS = {
    "c2d-standard-2": "#386cb0",
    "c2d-standard-4": "#fdb462",
    "c2d-standard-8": "#7fc97f",
}

# ================= HELPERS =================
def extract_users(fname):
    return int(re.search(r"users_(\d+)", fname).group(1))

def get_benchmark_df(df):
    df = df.copy()
    df["response_end"] = df["timeStamp"] + df["elapsed"]

    start_est = df["timeStamp"].min() + DELTA * 1000
    valid = df[df["response_end"] > start_est]

    if valid.empty:
        return pd.DataFrame(columns=df.columns)

    start = valid["response_end"].min()
    end = start + TOTAL_TIME * 1000

    return df[(df["response_end"] >= start) & (df["response_end"] <= end)]

def compute_latency(df):
    if len(df) == 0:
        return None
    df = df[df["responseCode"] == 200]
    if len(df) == 0:
        return None
    return df["elapsed"].median()

# ================= LOAD DATA =================
rows = []

for machine_dir in BASE_DIR.iterdir():
    if not machine_dir.is_dir():
        continue

    machine = machine_dir.name

    for impl_dir in machine_dir.iterdir():
        if not impl_dir.is_dir():
            continue

        implementation = impl_dir.name

        for iteration_dir in impl_dir.iterdir():
            if not iteration_dir.is_dir():
                continue

            for csv in iteration_dir.glob("users_*.csv"):
                df = pd.read_csv(csv)
                df["timeStamp"] -= df["timeStamp"].min()

                bench = get_benchmark_df(df)
                latency = compute_latency(bench)

                if latency is None:
                    continue

                rows.append({
                    "implementation": implementation,
                    "machine": machine,
                    "users": extract_users(csv.name),
                    "latency": latency
                })

df = pd.DataFrame(rows)

# ================= AGGREGATION =================
agg = (
    df.groupby(["implementation", "machine", "users"])["latency"]
    .median()
    .reset_index()
)

# ================= PLOTTING =================
plt.rcParams.update({
    "font.size": 12,
    "axes.edgecolor": "black",
    "axes.linewidth": 1,
})

for impl, impl_df in agg.groupby("implementation"):
    plt.figure(figsize=(9, 5))
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    for machine, mach_df in impl_df.groupby("machine"):
        mach_df = mach_df.sort_values("users")

        plt.plot(
            mach_df["users"],
            mach_df["latency"],
            marker="o",
            linewidth=2,
            label=machine,
            color=COLORS.get(machine)
        )

        # zaznaczenie minimum latency
        idx = mach_df["latency"].idxmin()
        x = mach_df.loc[idx, "users"]
        y = mach_df.loc[idx, "latency"]

        plt.scatter(x, y, color="black", marker="v", s=70, zorder=5)
        plt.annotate(
            f"{y:.1f}",
            (x, y),
            textcoords="offset points",
            xytext=(0, -18),
            ha="center",
            fontsize=10,
            fontweight="bold"
        )

    plt.title(impl, pad=20)
    plt.xlabel("Liczba użytkowników")
    plt.ylabel("Opóźnienie [ms]")
    plt.ylim(bottom=0)
    plt.grid(alpha=0.3)
    plt.legend(title="Typ maszyny", loc="upper left")

    plt.tight_layout(rect=[0, 0, 1, 0.97])
    plt.savefig(OUT_DIR / f"{impl}_vertical_scaling_latency.svg", format="svg")
    plt.close()