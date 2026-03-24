import matplotlib.pyplot as plt
from pathlib import Path

OUT_DIR = Path("plots-images")
OUT_DIR.mkdir(parents=True, exist_ok=True)

labels = [
    "IEEE Xplore",
    "SpringerLink",
    "ACM Digital Library",
    "ScienceDirect",
    "MDPI",
    "CEUR-WS"
]

sizes = [9, 3, 1, 1, 1, 1]

plt.figure(figsize=(8, 8))

plt.pie(
    sizes,
    labels=labels,
    autopct='%1.2f%%',
    startangle=90,
    wedgeprops={"edgecolor": "white"},
    textprops={"fontsize": 13}
)

plt.title("Udział poszczególnych źródeł publikacyjnych w końcowym zbiorze", pad=20, fontsize= 15)

plt.axis('equal')

output_path = OUT_DIR / "wykres_zrodla_publikacji.svg"
plt.savefig(output_path, format="svg", bbox_inches="tight")

plt.close()

print(output_path.resolve())