import numpy as np
import pandas as pd

def summarise_distribution(array_2d, years):
    return pd.DataFrame({
        "year": years,
        "mean": array_2d.mean(axis=0),
        "p5": np.percentile(array_2d, 5, axis=0),
        "p50": np.percentile(array_2d, 50, axis=0),
        "p95": np.percentile(array_2d, 95, axis=0),
    })

def cumulative_summary(array_2d):
    total = array_2d.sum(axis=1)
    return {
        "mean": total.mean(),
        "p5": np.percentile(total, 5),
        "p50": np.percentile(total, 50),
        "p95": np.percentile(total, 95),
    }

def riskiest_years(summary_df, n=5):
    df = summary_df.copy()
    df["width_p95_p5"] = df["p95"] - df["p5"]
    return df.nlargest(n, "width_p95_p5")
