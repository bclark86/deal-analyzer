import pytest
import numpy as np


def test_investor_waterfall(analyzer):
    noi = analyzer.investor_waterfall['net_operating_income']
    true_noi = [125_796.72, 129_569.59, 133_456.68, 137_460.38, 141_584.19]
    assert noi.tolist() == pytest.approx(true_noi, abs=1)
    assert analyzer.sell_price == pytest.approx(1_415_842, abs=1)
