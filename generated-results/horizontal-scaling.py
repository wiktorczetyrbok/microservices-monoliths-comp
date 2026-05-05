import re
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# ================= CONFIG =================
BASE_DIR = Path("results/horizontal-scaling")
OUT_DIR = Path("plots-images/horizontal-scaling")
OUT_DIR.mkdir(parents=True, exist_ok=True)

DELTA = 4          # sekundy do odcięcia ramp-up
TOTAL_TIME = 5     # sekundy pomiaru

COLORS = {
    "1-instance": "#386cb0",
    "2-instance": "#fdb462",
    "4-instance": "#7fc97f",
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

# ================= LOAD DATA =================
rows = []

for instance_dir in BASE_DIR.iterdir():  # 1-instance, 2-instance, 4-instance
    if not instance_dir.is_dir():
        continue

    instance = instance_dir.name

    for impl_dir in instance_dir.iterdir():  # java-microservices-grpc-images
        if not impl_dir.is_dir():
            continue

        implementation = impl_dir.name

        for iteration_dir in impl_dir.iterdir():  # 1 / 2 / 3 iteracje
            if not iteration_dir.is_dir():
                continue

            for csv in iteration_dir.glob("users_*.csv"):
                df = pd.read_csv(csv)
                df["timeStamp"] -= df["timeStamp"].min()

                bench = get_benchmark_df(df)
                thr = compute_throughput(bench)

                rows.append({
                    "implementation": implementation,
                    "instance": instance,
                    "users": extract_users(csv.name),
                    "throughput": thr
                })

df = pd.DataFrame(rows)

# ================= AGGREGATION =================
agg = (
    df.groupby(["implementation", "instance", "users"])
    .median()
    .reset_index()
)

# ================= PLOTTING =================
plt.rcParams.update({
    "font.size": 12,
    "axes.edgecolor": "black",
    "axes.linewidth": 0.5,
})

for impl, impl_df in agg.groupby("implementation"):

    plot_title = (
        impl
        .replace("-grpc-images", "")
        .replace("-images", "")
    )

    plt.figure(figsize=(9, 5))
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    for instance, inst_df in impl_df.groupby("instance"):
        inst_df = inst_df.sort_values("users")

        plt.plot(
            inst_df["users"],
            inst_df["throughput"],
            marker="o",
            linewidth=2,
            label=instance,
            color=COLORS.get(instance)
        )

        idx = inst_df["throughput"].idxmax()
        x = inst_df.loc[idx, "users"]
        y = inst_df.loc[idx, "throughput"]

        plt.scatter(x, y, color="black", marker="^", s=70, zorder=5)
        plt.annotate(
            f"{y:.1f}",
            (x, y),
            textcoords="offset points",
            xytext=(0, 10),
            ha="center",
            fontsize=10,
            fontweight="bold"
        )

    plt.title(plot_title, pad=20)
    plt.xlabel("Liczba użytkowników")
    plt.ylabel("Przepustowość [req/s]")
    plt.ylim(bottom=0)
    plt.grid(alpha=0.3)
    plt.legend(title="Instancje", loc="lower right")

    plt.tight_layout(rect=[0, 0, 1, 0.97])

    plt.savefig(OUT_DIR / f"{impl}_horizontal_scaling.pdf", format="pdf")
    plt.close()