import re
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# ================= CONFIG =================
# wybierz katalog bazowy:
# np. dla horizontal baseline:
BASE_DIR = Path("results/horizontal-scaling/1-instance")

# albo dla vertical baseline:
# BASE_DIR = Path("results/vertical-scaling/c2d-standard-2")

OUT_DIR = Path("plots-images/baseline-latency")
OUT_DIR.mkdir(parents=True, exist_ok=True)

DELTA = 4
TOTAL_TIME = 5

TITLE = "Monolit"   # albo np. "Mikroserwisy GRPC"
OUTPUT_FILE = "baseline_latency.svg"

COLORS = {
    "csharp": "#2b6cb0",
    "golang": "#e53e3e",
    "java": "#f6ad55",
    "python": "#68d391",
    "nodejs": "#805ad5",
    "javascript": "#805ad5",
}

LABELS = {
    "csharp": "C#",
    "golang": "GoLang",
    "java": "Java",
    "python": "Python",
    "nodejs": "Node.js",
    "javascript": "JavaScript",
}

# ================= HELPERS =================
def extract_users(fname):
    match = re.search(r"users_(\d+)", fname)
    return int(match.group(1)) if match else None

def normalize_impl_name(name: str) -> str:
    n = name.lower()

    if "csharp" in n or "c#" in n or "dotnet" in n:
        return "csharp"
    if "golang" in n or "go-" in n or n.startswith("go"):
        return "golang"
    if "java" in n:
        return "java"
    if "python" in n:
        return "python"
    if "node" in n or "javascript" in n or "js-" in n:
        return "nodejs"

    return n

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
    if df.empty:
        return None

    df = df[df["responseCode"] == 200]
    if df.empty:
        return None

    return df["elapsed"].median()

# ================= LOAD DATA =================
rows = []

for impl_dir in BASE_DIR.iterdir():
    if not impl_dir.is_dir():
        continue

    implementation_raw = impl_dir.name
    implementation = normalize_impl_name(implementation_raw)

    for iteration_dir in impl_dir.iterdir():
        if not iteration_dir.is_dir():
            continue

        for csv in iteration_dir.glob("users_*.csv"):
            users = extract_users(csv.name)
            if users is None:
                continue

            df = pd.read_csv(csv)
            df["timeStamp"] = df["timeStamp"] - df["timeStamp"].min()

            bench = get_benchmark_df(df)
            latency = compute_latency(bench)

            if latency is None:
                continue

            rows.append({
                "implementation": implementation,
                "users": users,
                "latency": latency
            })

if not rows:
    raise ValueError(f"No data found in {BASE_DIR}")

df = pd.DataFrame(rows)

# ================= AGGREGATION =================
agg = (
    df.groupby(["implementation", "users"])["latency"]
      .median()
      .reset_index()
)

# ================= PLOTTING =================
plt.rcParams.update({
    "font.size": 12,
    "axes.edgecolor": "black",
    "axes.linewidth": 1.0,
})

plt.figure(figsize=(10, 6))
ax = plt.gca()

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

for impl, impl_df in agg.groupby("implementation"):
    impl_df = impl_df.sort_values("users")

    plt.plot(
        impl_df["users"],
        impl_df["latency"],
        marker="o",
        markersize=3,
        linewidth=2.2,
        label=LABELS.get(impl, impl),
        color=COLORS.get(impl)
    )

plt.title(TITLE, pad=14, fontweight="bold")
plt.xlabel("Liczba użytkowników", fontweight="bold")
plt.ylabel("Mediana latencji (ms)", fontweight="bold")
plt.grid(True, alpha=0.25)
plt.legend(
    title="Implementacja",
    loc="lower center",
    bbox_to_anchor=(0.5, -0.18),
    ncol=5,
    frameon=False
)

plt.tight_layout()
plt.savefig(OUT_DIR / OUTPUT_FILE, format="svg", bbox_inches="tight")
plt.close()