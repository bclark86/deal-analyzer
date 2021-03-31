import pytest
import numpy as np


def test_noi(analyzer):
    noi = analyzer.investor_waterfall['net_operating_income']
    true_noi = [125_796.72, 129_569.59, 133_456.68, 137_460.38, 141_584.19]
    assert noi.tolist() == pytest.approx(true_noi, abs=1)
    assert analyzer.sell_price == pytest.approx(1_415_842, abs=1)


def test_cfaf(analyzer):
    true_cfaf =  [59_996.48, 63_770.35, 67_657.44, 71_661.14, 75_784.95]
    cfaf = analyzer.investor_waterfall['cash_flow_after_financing']
    assert cfaf.tolist() == pytest.approx(true_cfaf, abs=1)


def test_net_book_value(analyzer):
    assert analyzer.net_book_value == pytest.approx(1_194_127.54, abs=1)


def test_total_taxes(analyzer):
    assert analyzer.total_taxes == pytest.approx(52_024.69, abs=1)


def test_net_cash_from_sale(analyzer):
    assert analyzer.net_cash_from_sale == pytest.approx(478_325.51, abs=1)


def test_net_cash_flows(analyzer):
    true_cash_flows = [-337_388.50, 59_996.48, 63_770.35, 67_657.44, 71_661.14, 554_110.46]
    cash_flows = analyzer.investor_waterfall['net_cash_flows']
    assert cash_flows == pytest.approx(true_cash_flows, abs=1)


def test_deal_irr(analyzer):
    assert analyzer.investor_waterfall['deal_irr'] == pytest.approx(0.2470, abs=0.001)


def test_investor_cash_flows(analyzer):
    true_investor_cash_flows = [-303_648.75, 42_144.19, 44_031.13, 45_974.67, 47_976.52,  441_025.55]
    investor_cash_flows = analyzer.investor_waterfall['investor']['cash_flows']
    assert investor_cash_flows == pytest.approx(true_investor_cash_flows, abs=1)


def test_investor_irr(analyzer):
    assert analyzer.investor_waterfall['investor']['irr'] == pytest.approx(0.1889, abs=0.001)


def test_sponsor_irr(analyzer):
    assert analyzer.investor_waterfall['sponsor']['irr'] == pytest.approx(0.6778, abs=0.001)
