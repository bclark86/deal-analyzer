import numpy as np
import pandas as pd
from deal_analyzer.analyzer import DealAnalyzer


def sensitivity_analysis_trial(col, deal_specs, noise_pct=0.05):
    deal_specs_rv = deal_specs.copy()
    value = deal_specs_rv[col]
    noise = value * noise_pct
    deal_specs_rv[col] = np.random.triangular(
        left=value - noise, mode=value, right=value + noise
    )
    analyzer_rv = DealAnalyzer(**deal_specs_rv)
    return {
        "variable": col,
        "value": deal_specs_rv[col],
        "deal_irr": analyzer_rv.investor_waterfall["deal_irr"],
        "investor_irr": analyzer_rv.investor_waterfall["investor"]["irr"],
        "investor_cash_in": analyzer_rv.investor_waterfall["investor"][
            "contribution"
        ],
        "investor_cash_out": analyzer_rv.investor_waterfall["investor"][
            "cash_flows"
        ].sum(),
        "sponsor_irr": analyzer_rv.investor_waterfall["sponsor"]["irr"],
        "sponsor_cash_in": analyzer_rv.investor_waterfall["sponsor"][
            "contribution"
        ],
        "sponsor_cash_out": analyzer_rv.investor_waterfall["sponsor"][
            "cash_flows"
        ].sum(),
    }


def sensitivity_analysis_experiment(col, deal_specs, k=10_000, noise_pct=0.05):
    return pd.DataFrame(
        [
            sensitivity_analysis_trial(col, deal_specs, noise_pct=noise_pct)
            for _ in range(k)
        ]
    )


def run_sensitivity_analysis(search_cols, deal_specs, noise_pct=0.05):
    return pd.concat(
        [
            sensitivity_analysis_experiment(
                col, deal_specs, k=10_000, noise_pct=noise_pct
            )
            for col in search_cols
        ],
        ignore_index=True,
    )
