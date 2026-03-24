import matplotlib.pyplot as plt
import re
from pathlib import Path
OUT_DIR = Path("plots-images/vertical-scaling")
OUT_DIR.mkdir(parents=True, exist_ok=True)
years = [2017,2018,2019, 2020, 2021, 2022, 2023, 2024, 2025]
counts = [1,0,0 ,2, 2, 3, 4, 2, 2]

plt.figure(figsize=(9, 5.2))
bars = plt.bar(years, counts, width=0.65)

plt.title("Liczba wybranych publikacji w zależności od roku wydania", pad=14)
plt.xlabel("Rok wydania")
plt.ylabel("Liczba publikacji")
plt.xticks(years)
plt.yticks(range(0, max(counts) + 2))
plt.ylim(0, max(counts) + 1)

for bar, value in zip(bars, counts):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        value + 0.05,
        str(value),
        ha="center",
        va="bottom",
        fontsize=10
    )

plt.tight_layout()

png_path = "/wykres_publikacje_lata.png"
svg_path = "wykres_publikacje_lata.svg"

# plt.savefig(png_path, dpi=300, bbox_inches="tight")
plt.savefig(OUT_DIR / svg_path, bbox_inches="tight")
plt.show()

print(png_path)
print(svg_path)