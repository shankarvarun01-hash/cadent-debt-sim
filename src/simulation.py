import numpy as np
import pandas as pd

def prepare_rate_matrix(scen_df, scenario_col="scenario", year_col="year", rate_col="sonia_rate", horizon_years=30):
    rate_matrix = (
        scen_df.pivot(index=scenario_col, columns=year_col, values=rate_col)
        .sort_index()
        .sort_index(axis=1)
    )
    last_col = rate_matrix.columns.max()
    for y in range(last_col + 1, horizon_years):
        rate_matrix[y] = rate_matrix[last_col]
    return rate_matrix[sorted(rate_matrix.columns)]

def annual_coupon(rate_type, coupon_or_spread, market_rate):
    if rate_type == "fixed":
        return coupon_or_spread
    if rate_type in ["floating_sonia", "floating_base"]:
        return market_rate + coupon_or_spread
    raise ValueError(f"Unknown rate_type: {rate_type}")

def simulate_runoff(debt_df, rate_matrix, start_year=2025, horizon_years=30):
    n_scen = rate_matrix.shape[0]
    interest = np.zeros((n_scen, horizon_years))
    outstanding = np.zeros((n_scen, horizon_years))

    for t in range(horizon_years):
        cal_year = start_year + t
        market_rates = rate_matrix.iloc[:, t].values

        alive = debt_df["maturity_year"].values >= cal_year
        outstanding_amt = debt_df.loc[alive, "notional_gbp_m"].sum()
        outstanding[:, t] = outstanding_amt

        fixed_mask = alive & (debt_df["rate_type"].values == "fixed")
        float_mask = alive & (debt_df["rate_type"].values != "fixed")

        fixed_interest = (
            debt_df.loc[fixed_mask, "notional_gbp_m"] *
            debt_df.loc[fixed_mask, "coupon_or_spread"]
        ).sum()

        float_notional = debt_df.loc[float_mask, "notional_gbp_m"].values
        float_spreads = debt_df.loc[float_mask, "coupon_or_spread"].values

        float_interest = np.zeros(n_scen)
        if len(float_notional) > 0:
            float_interest = (market_rates[:, None] + float_spreads[None, :]) @ float_notional

        interest[:, t] = fixed_interest + float_interest

    return interest, outstanding

def simulate_full_refinancing(debt_df, rate_matrix, start_year=2025, horizon_years=30, refi_term=20):
    n_scen = rate_matrix.shape[0]
    interest = np.zeros((n_scen, horizon_years))
    outstanding = np.zeros((n_scen, horizon_years))

    base_records = debt_df[["notional_gbp_m", "rate_type", "coupon_or_spread", "maturity_year"]].to_dict("records")

    for s in range(n_scen):
        portfolio = [dict(r) for r in base_records]

        for t in range(horizon_years):
            cal_year = start_year + t
            market_rate = rate_matrix.iloc[s, t]

            annual_interest = 0.0
            annual_outstanding = 0.0
            matured_notional = 0.0
            survivors = []

            for tr in portfolio:
                if tr["maturity_year"] >= cal_year:
                    annual_outstanding += tr["notional_gbp_m"]
                    annual_interest += tr["notional_gbp_m"] * annual_coupon(
                        tr["rate_type"], tr["coupon_or_spread"], market_rate
                    )

                    if tr["maturity_year"] == cal_year:
                        matured_notional += tr["notional_gbp_m"]
                    else:
                        survivors.append(tr)

            if matured_notional > 0:
                survivors.append({
                    "notional_gbp_m": matured_notional,
                    "rate_type": "fixed",
                    "coupon_or_spread": market_rate,
                    "maturity_year": cal_year + refi_term,
                })

            portfolio = survivors
            interest[s, t] = annual_interest
            outstanding[s, t] = annual_outstanding

    return interest, outstanding
