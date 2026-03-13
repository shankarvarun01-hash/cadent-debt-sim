import pandas as pd
import numpy as np

VAL_DATE = pd.Timestamp("2024-12-31")

def load_debt_table():
    rows = [
        ("Related party loan OD 1", 255, "floating_base", 0.0100, "2025-06-30", "Base + 1%"),
        ("Related party loan OD 2",  64, "floating_base", 0.03507, "2025-06-30", "Base + 3.507%"),
        ("Related party loan OD 3",   3, "floating_base", 0.0100, "2025-06-30", "Base + 1%"),
        ("Related party loan", 700, "floating_sonia", 0.0075, "2025-01-31", "SONIA + CAS + 0.75%"),
        ("Related party loan", 500, "fixed", 0.04106, "2025-08-01", "4.106%"),
        ("Related party loan current amort", 190, "floating_sonia", 0.0078, "2025-12-31", "SONIA + CAS + 0.78%"),
        ("Related party loan residual", 190, "floating_sonia", 0.0078, "2027-12-20", "SONIA + CAS + 0.78%"),
        ("Related party loan", 800, "floating_sonia", 0.0056, "2029-05-22", "SONIA + CAS + 0.56%"),
        ("Related party loan", 500, "fixed", 0.04454, "2029-08-01", "4.454%"),
        ("Related party loan", 500, "floating_sonia", 0.0121, "2030-12-20", "SONIA + 1.21%"),
        ("Related party loan", 500, "floating_sonia", 0.0069, "2031-02-22", "SONIA + CAS + 0.69%"),
        ("Related party loan", 800, "fixed", 0.043835, "2032-03-30", "4.3835%"),
        ("Related party loan", 300, "floating_sonia", 0.0175, "2032-07-29", "SONIA + 1.75%"),
        ("Related party loan", 500, "fixed", 0.03745, "2032-08-01", "3.745%"),
        ("Related party loan", 700, "floating_sonia", 0.0143, "2033-12-20", "SONIA + 1.43%"),
        ("Related party loan", 600, "fixed", 0.05358, "2034-10-31", "5.358%"),
        ("Related party loan", 815, "floating_sonia", 0.0147, "2035-10-21", "SONIA + 1.47%"),
        ("€350m euro-sterling bond", 350, "fixed", 0.05875, "2026-07-17", "5.875%"),
        ("€350m euro-sterling bond", 349, "fixed", 0.04875, "2027-09-20", "4.875%"),
        ("10bn JPY loan", 60, "fixed", 0.04600, "2029-07-27", "4.6%"),
        ("€350m euro-sterling bond", 344, "fixed", 0.02000, "2031-11-13", "2.0%"),
        ("£50m medium-term note", 50, "fixed", 0.05750, "2039-12-09", "5.75%"),
        ("£100m medium-term note", 100, "fixed", 0.06375, "2041-03-31", "6.375%"),
    ]
    df = pd.DataFrame(
        rows,
        columns=["instrument", "notional_gbp_m", "rate_type", "coupon_or_spread", "maturity_date", "rate_label"]
    )
    df["maturity_date"] = pd.to_datetime(df["maturity_date"])
    df["maturity_year"] = df["maturity_date"].dt.year
    df["years_to_maturity"] = (df["maturity_date"] - VAL_DATE).dt.days / 365.25
    return df

def debt_summary(df):
    total_notional = df["notional_gbp_m"].sum()
    rate_mix = (df.groupby("rate_type")["notional_gbp_m"].sum() / total_notional).to_dict()
    wam = np.average(df["years_to_maturity"], weights=df["notional_gbp_m"])
    return {
        "total_notional_gbp_m": total_notional,
        "weighted_average_maturity_years": wam,
        "pct_fixed": rate_mix.get("fixed", 0.0),
        "pct_floating_sonia": rate_mix.get("floating_sonia", 0.0),
        "pct_floating_base": rate_mix.get("floating_base", 0.0),
    }
