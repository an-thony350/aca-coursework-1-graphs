"""plot ACA Section 1 energy results"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.ticker import FormatStrFormatter


HERE = Path(__file__).resolve().parent
CSV = HERE / "section1_rob_intregs_energy.csv"
OUTPUT = HERE / "figures" / "plot_line_graph.pdf"

ROB_SIZES = (16, 32, 64, 128, 256)
REG_COUNTS = (49, 62, 75, 88, 101)
STYLES = {
    16: dict(color="#3564A0", marker="o", linestyle="-"),
    32: dict(color="#D07932", marker="s", linestyle="--"),
    64: dict(color="#07877F", marker="D", linestyle="-"),
    128: dict(color="#8055A3", marker="^", linestyle="-."),
    256: dict(color="#BE4C72", marker="v", linestyle=":"),
}


def main():
    data = pd.read_csv(CSV).sort_values(["rob_entries", "int_physical_registers"])
    best = data.loc[data["energy_j"].idxmin()]

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

    fig, (main_ax, zoom_ax) = plt.subplots(
        2, 1, figsize=(8.3, 10.6), gridspec_kw={"height_ratios": [1, 1.1]}
    )
    fig.subplots_adjust(left=0.12, right=0.97, top=0.875,
                        bottom=0.105, hspace=0.35)

    for ax in (main_ax, zoom_ax):
        ax.set_axisbelow(True)
        ax.grid(axis="y", color="#E1E7EC", linewidth=0.9)
        ax.spines[["top", "right"]].set_visible(False)
        ax.set_ylabel("Energy consumption (J)")
        ax.tick_params(axis="both", length=0, pad=7)

    # Full sweep above; magnified high-register region below.
    for ax, rob_sizes, min_regs in (
        (main_ax, ROB_SIZES, 49),
        (zoom_ax, (64, 128, 256), 75),
    ):
        for rob in rob_sizes:
            rows = data[(data["rob_entries"] == rob) &
                        (data["int_physical_registers"] >= min_regs)]
            ax.plot(rows["int_physical_registers"], rows["energy_j"],
                    **STYLES[rob], markersize=6.6, markeredgecolor="white",
                    markeredgewidth=0.8, linewidth=2.25, zorder=3)
        ax.scatter(best["int_physical_registers"], best["energy_j"],
                   s=230, facecolors="none", edgecolors="#1B2631",
                   linewidths=1.6, zorder=8)

    main_ax.set_title("All 25 configurations", loc="left", pad=10)
    main_ax.set_xticks(REG_COUNTS)
    main_ax.set_xlim(46.5, 103.5)
    main_ax.set_ylim(0.237, 0.378)
    main_ax.set_yticks([0.24, 0.26, 0.28, 0.30, 0.32, 0.34, 0.36])

    zoom_ax.set_title("Magnified detail: ROB 64, 128 and 256", loc="left", pad=10)
    zoom_ax.set_xlim(73, 103.5)
    zoom_ax.set_xticks([75, 88, 101])
    zoom_ax.set_ylim(0.2418, 0.2522)
    zoom_ax.set_yticks([0.242, 0.244, 0.246, 0.248, 0.250, 0.252])
    zoom_ax.yaxis.set_major_formatter(FormatStrFormatter("%.3f"))
    zoom_ax.set_xlabel("Integer physical registers", labelpad=9)

    handles = [Line2D([0], [0], label=f"ROB {rob}", linewidth=2.3,
                      markersize=6.5, **STYLES[rob]) for rob in ROB_SIZES]
    fig.legend(handles=handles, ncol=5, loc="upper center",
               bbox_to_anchor=(0.545, 0.965), frameon=False,
               title="ROB entries", fontsize=10, title_fontsize=10,
               handlelength=3.2, columnspacing=1.8)
    fig.text(0.12, 0.047,
             f"Circled minimum: ROB {int(best['rob_entries'])}, "
             f"{int(best['int_physical_registers'])} registers, "
             f"{best['energy_j']:.6f} J. Both y-axes are truncated.",
             ha="left", va="center", fontsize=9.4, color="#4B5D6B")

    OUTPUT.parent.mkdir(exist_ok=True)
    fig.savefig(OUTPUT, bbox_inches="tight", pad_inches=0.16)
    plt.close(fig)
    print(f"Saved {OUTPUT}")


if __name__ == "__main__":
    main()
