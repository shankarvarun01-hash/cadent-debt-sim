import matplotlib.pyplot as plt

def plot_maturity_wall(maturity_wall, output_path=None):
    ax = maturity_wall.plot(kind="bar", stacked=True, figsize=(10, 5))
    ax.set_title("Debt maturity wall")
    ax.set_xlabel("Maturity year")
    ax.set_ylabel("Notional (£m)")
    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=200)
    plt.show()

def plot_runoff_outstanding(runoff_curve, output_path=None):
    plt.figure(figsize=(10, 5))
    plt.plot(runoff_curve["year"], runoff_curve["outstanding_gbp_m"])
    plt.title("Outstanding notional under run-off")
    plt.xlabel("Year")
    plt.ylabel("Outstanding (£m)")
    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=200)
    plt.show()

def plot_interest_regimes(runoff_stats, refi_stats, output_path=None):
    plt.figure(figsize=(10, 5))
    plt.plot(runoff_stats["year"], runoff_stats["mean"], label="Run-off mean")
    plt.fill_between(runoff_stats["year"], runoff_stats["p5"], runoff_stats["p95"], alpha=0.2)
    plt.plot(refi_stats["year"], refi_stats["mean"], label="Full refinancing mean")
    plt.fill_between(refi_stats["year"], refi_stats["p5"], refi_stats["p95"], alpha=0.2)
    plt.title("Annual portfolio interest cost by regime")
    plt.xlabel("Year")
    plt.ylabel("Interest cost (£m)")
    plt.legend()
    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=200)
    plt.show()
