import re
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.ticker import MultipleLocator

HORIZONTAL_BASE_DIR = Path("results/horizontal-scaling")
VERTICAL_BASE_DIR = Path("results/vertical-scaling")
OUT_DIR = Path("plots-images/scaling-comparison")
OUT_DIR.mkdir(parents=True, exist_ok=True)

DELTA = 4
TOTAL_TIME = 5

HORIZONTAL_COLOR = "#E6C229"
VERTICAL_COLOR = "#2E7D32"

LANGUAGE_ORDER = ["javascript", "python", "java"]

IMPLEMENTATION_LABELS = {
    "microservices-grpc": "Mikroserwisy gRPC",
    "monolith": "Monolit",
}

IMPLEMENTATION_ORDER = [
    "microservices-grpc",
    "monolith",
]

HORIZONTAL_RESOURCE_MAP = {
    "1-instance": 1,
    "2-instance": 2,
    "4-instance": 4,
}

VERTICAL_RESOURCE_MAP = {
    "c2d-standard-2": 2,
    "c2d-standard-4": 4,
    "c2d-standard-8": 8,
}

plt.rcParams.update({
    "font.size": 11,
    "axes.titlesize": 12,
    "axes.labelsize": 12
})

def extract_users(fname: str) -> int:
    match = re.search(r"users_(\d+)", fname)
    if not match:
        raise ValueError(f"Nie można odczytać liczby użytkowników z nazwy pliku: {fname}")
    return int(match.group(1))

def get_benchmark_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["response_end"] = df["timeStamp"] + df["elapsed"]
    start_est = df["timeStamp"].min() + DELTA * 1000
    valid = df[df["response_end"] > start_est]
    if valid.empty:
        return df.iloc[0:0]
    start = valid["response_end"].min()
    end = start + TOTAL_TIME * 1000
    return df[(df["response_end"] >= start) & (df["response_end"] <= end)]

def compute_throughput(df: pd.DataFrame) -> float:
    if df.empty:
        return 0.0
    df = df[df["responseCode"] == 200]
    return len(df) / TOTAL_TIME

def parse_implementation_name(implementation: str):
    if implementation.endswith("-images"):
        implementation = implementation[:-7]
    parts = implementation.split("-")
    if len(parts) < 2:
        return None, None
    language = parts[0]
    if "microservices" in parts and "grpc" in parts:
        impl_type = "microservices-grpc"
    elif "monolith" in parts:
        impl_type = "monolith"
    else:
        return language, None
    return language, impl_type

def prettify_language(lang: str) -> str:
    mapping = {
        "python": "Python",
        "java": "Java",
        "javascript": "JavaScript",
        "js": "JavaScript",
    }
    return mapping.get(lang, lang.capitalize())

def load_horizontal_data(base_dir: Path) -> pd.DataFrame:
    rows = []
    for instance_dir in base_dir.iterdir():
        if not instance_dir.is_dir():
            continue
        instance = instance_dir.name
        if instance not in HORIZONTAL_RESOURCE_MAP:
            continue
        for impl_dir in instance_dir.iterdir():
            if not impl_dir.is_dir():
                continue
            implementation = impl_dir.name
            language, impl_type = parse_implementation_name(implementation)
            if not language or not impl_type:
                continue
            for iteration_dir in impl_dir.iterdir():
                if not iteration_dir.is_dir():
                    continue
                for csv in iteration_dir.glob("users_*.csv"):
                    df = pd.read_csv(csv)
                    df["timeStamp"] -= df["timeStamp"].min()
                    bench = get_benchmark_df(df)
                    thr = compute_throughput(bench)
                    rows.append({
                        "scaling_type": "horizontal",
                        "language": language,
                        "implementation": impl_type,
                        "resource_level": HORIZONTAL_RESOURCE_MAP[instance],
                        "users": extract_users(csv.name),
                        "throughput": thr
                    })
    if not rows:
        return pd.DataFrame(columns=[
            "scaling_type", "language", "implementation",
            "resource_level", "users", "throughput"
        ])
    df = pd.DataFrame(rows)
    agg = (
        df.groupby(["scaling_type", "language", "implementation", "resource_level", "users"], as_index=False)
          .median(numeric_only=True)
    )
    return agg

def load_vertical_data(base_dir: Path) -> pd.DataFrame:
    rows = []
    for machine_dir in base_dir.iterdir():
        if not machine_dir.is_dir():
            continue
        machine = machine_dir.name
        if machine not in VERTICAL_RESOURCE_MAP:
            continue
        for impl_dir in machine_dir.iterdir():
            if not impl_dir.is_dir():
                continue
            implementation = impl_dir.name
            language, impl_type = parse_implementation_name(implementation)
            if not language or not impl_type:
                continue
            for iteration_dir in impl_dir.iterdir():
                if not iteration_dir.is_dir():
                    continue
                for csv in iteration_dir.glob("users_*.csv"):
                    df = pd.read_csv(csv)
                    df["timeStamp"] -= df["timeStamp"].min()
                    bench = get_benchmark_df(df)
                    thr = compute_throughput(bench)
                    rows.append({
                        "scaling_type": "vertical",
                        "language": language,
                        "implementation": impl_type,
                        "resource_level": VERTICAL_RESOURCE_MAP[machine],
                        "users": extract_users(csv.name),
                        "throughput": thr
                    })
    if not rows:
        return pd.DataFrame(columns=[
            "scaling_type", "language", "implementation",
            "resource_level", "users", "throughput"
        ])
    df = pd.DataFrame(rows)
    agg = (
        df.groupby(["scaling_type", "language", "implementation", "resource_level", "users"], as_index=False)
          .median(numeric_only=True)
    )
    return agg

def get_max_throughput(df: pd.DataFrame, scaling_type: str, language: str, implementation: str, resource_level: int):
    subset = df[
        (df["scaling_type"] == scaling_type) &
        (df["language"] == language) &
        (df["implementation"] == implementation) &
        (df["resource_level"] == resource_level)
    ]
    if subset.empty:
        return None
    idx = subset["throughput"].idxmax()
    return float(subset.loc[idx, "throughput"])

def build_plot_dataframe(all_data: pd.DataFrame) -> pd.DataFrame:
    rows = []
    languages = [lang for lang in LANGUAGE_ORDER if lang in all_data["language"].unique()]
    remaining = sorted(set(all_data["language"].unique()) - set(languages))
    languages.extend(remaining)
    for language in languages:
        for implementation in IMPLEMENTATION_ORDER:
            h_2x = get_max_throughput(all_data, "horizontal", language, implementation, 2)
            v_2x = get_max_throughput(all_data, "vertical", language, implementation, 4)
            h_4x = get_max_throughput(all_data, "horizontal", language, implementation, 4)
            v_4x = get_max_throughput(all_data, "vertical", language, implementation, 8)
            if any(x is not None for x in [h_2x, v_2x, h_4x, v_4x]):
                rows.append({
                    "language": language,
                    "implementation": implementation,
                    "horizontal_2x": h_2x,
                    "vertical_2x": v_2x,
                    "horizontal_4x": h_4x,
                    "vertical_4x": v_4x,
                })
    return pd.DataFrame(rows)

def plot_language_comparison(language: str, lang_df: pd.DataFrame, out_dir: Path):
    if lang_df.empty:
        return
    h_2x, v_2x, h_4x, v_4x = [], [], [], []
    implementations_present = []
    for impl in IMPLEMENTATION_ORDER:
        row = lang_df[lang_df["implementation"] == impl]
        if row.empty:
            continue
        implementations_present.append(impl)
        row = row.iloc[0]
        h_2x.append(row["horizontal_2x"])
        v_2x.append(row["vertical_2x"])
        h_4x.append(row["horizontal_4x"])
        v_4x.append(row["vertical_4x"])
    if not implementations_present:
        return
    plt.style.use("ggplot")
    fig, axes = plt.subplots(1, 2, figsize=(14.5, 7), sharey=False)
    bar_width = 0.44
    panels = [
        ("Dwukrotne zwiększenie zasobów", h_2x, v_2x),
        ("Czterokrotne zwiększenie zasobów", h_4x, v_4x),
    ]
    all_values = [v for values in [h_2x, v_2x, h_4x, v_4x] for v in values if pd.notna(v)]
    if not all_values:
        return
    y_max = max(all_values) * 1.12
    for ax, (panel_title, horizontal_vals, vertical_vals) in zip(axes, panels):
        x = list(range(len(horizontal_vals)))
        x1 = [i - bar_width / 2 for i in x]
        x2 = [i + bar_width / 2 for i in x]
        bars1 = ax.bar(x1, horizontal_vals, width=bar_width, color=HORIZONTAL_COLOR, label="Horyzontalne")
        bars2 = ax.bar(x2, vertical_vals, width=bar_width, color=VERTICAL_COLOR, label="Wertykalne")
        ax.set_xticks(x)
        ax.set_xticklabels(
            [IMPLEMENTATION_LABELS[i] for i in implementations_present],
            rotation=45,
            ha="right"
        )
        ax.set_ylim(0, y_max)
    
        ax.grid(axis="y", linestyle="--", alpha=0.3)
        rect = Rectangle((0, 0.945), 1, 0.06, transform=ax.transAxes,
                         color="#efefef", ec="none", zorder=-1, clip_on=False)
        ax.add_patch(rect)
        ax.text(0.5, 0.975, panel_title, transform=ax.transAxes,
                ha="center", va="center", fontsize=10, fontweight="bold")
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                if pd.isna(height):
                    continue
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    height + y_max * 0.01,
                    f"{height:.1f}",
                    ha="center",
                    va="bottom",
                    fontsize=10
                )
    fig.suptitle(f"Porównanie mechanizmów skalowania dla języka {prettify_language(language)}",
                 fontsize=16, fontweight="bold", y=0.98)
    axes[0].set_ylabel("Przepustowość", fontweight="bold")
    #fig.supxlabel("Implementacja aplikacji", y=0.09, fontweight="bold")
    handles, labels = axes[0].get_legend_handles_labels()
    legend = fig.legend(
        handles, labels,
        loc="lower center",
        ncol=2,
        frameon=False,
        bbox_to_anchor=(0.5, 0.01),
        title="Mechanizm skalowania",
        fontsize=12
    )
    legend.get_title().set_fontstyle("italic")
    plt.tight_layout(rect=[0, 0.15, 1, 0.94])
    out_path = out_dir / f"{language}_scaling_comparison.svg"
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close()

def main():
    horizontal_df = load_horizontal_data(HORIZONTAL_BASE_DIR)
    vertical_df = load_vertical_data(VERTICAL_BASE_DIR)
    all_data = pd.concat([horizontal_df, vertical_df], ignore_index=True)
    if all_data.empty:
        print("Brak danych do wygenerowania wykresów.")
        return
    plot_df = build_plot_dataframe(all_data)
    if plot_df.empty:
        print("Nie udało się zbudować zestawu danych do porównania.")
        return
    for language, lang_df in plot_df.groupby("language"):
        plot_language_comparison(language, lang_df, OUT_DIR)
        print(f"Zapisano wykres dla języka: {prettify_language(language)}")
    print(f"\nGotowe. Wykresy zapisano w folderze: {OUT_DIR}")

if __name__ == "__main__":
    main()