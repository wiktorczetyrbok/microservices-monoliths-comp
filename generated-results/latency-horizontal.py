import re
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

# ================= CONFIG =================
BASE_DIR = Path("JMeter/results/horizontal-scaling/1-instance")
OUT_DIR = Path("plots-images")
OUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = "latencja_wedlug_jezyka_i_implementacji.svg"

DELTA = 4
TOTAL_TIME = 5

TITLE = "Mediana latencji w zależności od języka i typu implementacji"

LANGUAGE_COLORS = {
    "java": "#e67e22",         # pomarańczowy
    "python": "#27ae60",       # zielony
    "javascript": "#8e44ad",   # fioletowy
}

IMPLEMENTATION_STYLES = {
    "monolith": "-",
    "microservices-grpc": "--",
    "microservices-rest": ":",
    "microservices": "--",
}

IMPLEMENTATION_MARKERS = {
    "monolith": "o",
    "microservices-grpc": "s",
    "microservices-rest": "^",
    "microservices": "s",
}

# ================= HELPERS =================
def extract_users(fname: str):
    match = re.search(r"users_(\d+)", fname)
    return int(match.group(1)) if match else None


def normalize_language(token: str):
    token = token.lower()
    if token == "java":
        return "java"
    if token == "python":
        return "python"
    if token in ("js", "javascript", "node", "nodejs"):
        return "javascript"
    return None


def language_label(language: str):
    return {
        "java": "Java",
        "python": "Python",
        "javascript": "JavaScript",
    }.get(language, language.capitalize())


def implementation_label(implementation: str):
    mapping = {
        "monolith": "Monolit",
        "microservices-grpc": "Mikroserwisy gRPC",
        "microservices-rest": "Mikroserwisy REST",
        "microservices": "Mikroserwisy",
    }
    return mapping.get(implementation, implementation.replace("-", " ").title())


def parse_impl_dir_name(dir_name: str):
    parts = [p for p in dir_name.lower().split("-") if p and p != "images"]
    if len(parts) < 2:
        return None

    language = normalize_language(parts[0])
    if language is None:
        return None

    implementation = "-".join(parts[1:])

    return {
        "language": language,
        "language_label": language_label(language),
        "implementation": implementation,
        "implementation_label": implementation_label(implementation),
        "series_label": f"{language_label(language)} – {implementation_label(implementation)}",
    }


def get_benchmark_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["response_end"] = df["timeStamp"] + df["elapsed"]

    start_est = df["timeStamp"].min() + DELTA * 1000
    valid = df[df["response_end"] > start_est]

    if valid.empty:
        return pd.DataFrame(columns=df.columns)

    start = valid["response_end"].min()
    end = start + TOTAL_TIME * 1000

    return df[(df["response_end"] >= start) & (df["response_end"] <= end)]


def compute_latency(df: pd.DataFrame):
    if df.empty:
        return None

    df = df.copy()
    df["responseCode"] = df["responseCode"].astype(str)
    df = df[df["responseCode"] == "200"]

    if df.empty:
        return None

    return df["elapsed"].median()


# ================= LOAD DATA =================
rows = []

for impl_dir in BASE_DIR.iterdir():
    if not impl_dir.is_dir():
        continue

    parsed = parse_impl_dir_name(impl_dir.name)
    if parsed is None:
        print(f"Pomijam nierozpoznany katalog: {impl_dir.name}")
        continue

    for csv in impl_dir.rglob("users_*.csv"):
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
            "language": parsed["language"],
            "language_label": parsed["language_label"],
            "implementation": parsed["implementation"],
            "implementation_label": parsed["implementation_label"],
            "series_label": parsed["series_label"],
            "users": users,
            "latency": latency,
        })

if not rows:
    raise ValueError(f"Nie znaleziono danych w katalogu: {BASE_DIR}")

df = pd.DataFrame(rows)

# ================= AGGREGATION =================
agg = (
    df.groupby(
        ["language", "implementation", "series_label", "users"],
        as_index=False
    )["latency"]
    .median()
)

series_order = [
    ("java", "monolith"),
    ("java", "microservices-grpc"),
    ("python", "monolith"),
    ("python", "microservices-grpc"),
    ("javascript", "monolith"),
    ("javascript", "microservices-grpc"),
]

# ================= PLOTTING =================
plt.rcParams.update({
    "font.size": 12,
    "axes.edgecolor": "black",
    "axes.linewidth": 1.0,
})

plt.figure(figsize=(14, 8))
ax = plt.gca()

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

for language, implementation in series_order:
    series_df = agg[
        (agg["language"] == language) &
        (agg["implementation"] == implementation)
    ].sort_values("users")

    if series_df.empty:
        continue

    plt.plot(
        series_df["users"],
        series_df["latency"],
        label=series_df["series_label"].iloc[0],
        color=LANGUAGE_COLORS.get(language, "#333333"),
        linestyle=IMPLEMENTATION_STYLES.get(implementation, "-"),
        marker=IMPLEMENTATION_MARKERS.get(implementation, "o"),
        markersize=4,
        linewidth=2.4,
    )

plt.title(TITLE, pad=16, fontweight="bold")
plt.xlabel("Liczba użytkowników", fontweight="bold")
plt.ylabel("Mediana latencji [ms]", fontweight="bold")
plt.grid(True, alpha=0.25)

plt.legend(
    title="Język i typ implementacji",
    loc="center left",
    bbox_to_anchor=(0.9, 0.5),
    frameon=False,
    fontsize=13,
    title_fontsize=14,
)

plt.tight_layout()
plt.savefig(OUT_DIR / OUTPUT_FILE, format="svg", bbox_inches="tight")
plt.close()

print(f"Zapisano wykres: {OUT_DIR / OUTPUT_FILE}")