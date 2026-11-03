"""plot ROB energy changes"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FixedLocator, FuncFormatter


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "figures" / "plot_rob_change.pdf"

LABELS = [r"16$\rightarrow$32", r"32$\rightarrow$64",
          r"64$\rightarrow$128", r"128$\rightarrow$256"]
CHANGES = [-21.616, -7.319, 0.466, 0.910]


def main():
    magnitudes = [abs(change) for change in CHANGES]
    x = range(len(CHANGES))

    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.labelsize": 12,
        "axes.titlesize": 12,
        "axes.edgecolor": "#AAB4BE",
        "axes.labelcolor": "#293746",
        "xtick.color": "#495A69",
        "ytick.color": "#495A69",
        "pdf.fonttype": 42,
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
    })

    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    ax.plot(x, magnitudes, color="#1f6f9f", linewidth=2, zorder=1)

    for i, (magnitude, change) in enumerate(zip(magnitudes, CHANGES)):
        decreasing = change < 0
        ax.scatter(i, magnitude, s=70, zorder=3,
                   marker="v" if decreasing else "^",
                   color="#2a9d5c" if decreasing else "#c0392b",
                   edgecolor="black", linewidth=0.6)
        ax.annotate(f"{change:+.2f}%", (i, magnitude),
                    textcoords="offset points",
                    xytext=(0, 10) if i != 2 else (14, -4),
                    ha="center" if i != 2 else "left", fontsize=10)

    # Highlight the smallest magnitude of energy change.
    ax.scatter(2, magnitudes[2], s=320, facecolor="none",
               edgecolor="#e6a700", linewidth=2, zorder=2)
    ax.annotate("Smallest change", (2, magnitudes[2]),
                textcoords="offset points", xytext=(-110, -40),
                fontsize=10, color="#9a7000",
                arrowprops=dict(arrowstyle="->", color="#9a7000"))

    ax.set_yscale("log")
    ax.set_ylim(0.1, 50)
    ax.yaxis.set_major_locator(FixedLocator([0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50]))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"{y:g}"))
    ax.set_xticks(list(x), LABELS)
    ax.set_xlim(-0.4, 3.4)
    ax.set_xlabel("Transition in number of ROB entries")
    ax.set_ylabel("Magnitude of change in\nenergy consumption (%, log scale)")
    ax.grid(True, which="major", linestyle="--", alpha=0.5)
    ax.grid(True, which="minor", linestyle=":", alpha=0.25)

    handles = [
        Line2D([], [], marker="v", linestyle="", color="#2a9d5c",
               markeredgecolor="black", markersize=8, label="Energy decrease"),
        Line2D([], [], marker="^", linestyle="", color="#c0392b",
               markeredgecolor="black", markersize=8, label="Energy increase"),
    ]
    ax.legend(handles=handles, loc="upper right", frameon=True)

    fig.tight_layout()
    OUTPUT.parent.mkdir(exist_ok=True)
    fig.savefig(OUTPUT)
    plt.close(fig)
    print(f"Saved {OUTPUT}")


if __name__ == "__main__":
    main()
