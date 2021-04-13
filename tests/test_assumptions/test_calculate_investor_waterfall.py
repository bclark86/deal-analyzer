import pytest
import numpy as np


def test_noi(analyzer):
    noi = analyzer.investor_waterfall['net_operating_income']
    true_noi = [129611.46, 133499.80, 137504.80, 141629.94, 145878.84]
    assert noi.tolist() == pytest.approx(true_noi, abs=1)
    assert analyzer.sell_price == pytest.approx(1_458_788.40, abs=1)


def test_cfaf(analyzer):
    true_cfaf = [63_812, 67701, 71706, 75831, 80080]
    cfaf = analyzer.investor_waterfall['cash_flow_after_financing']
    assert cfaf.tolist() == pytest.approx(true_cfaf, abs=1)


def test_net_book_value(analyzer):
    assert analyzer.net_book_value == pytest.approx(1179663.636, abs=1)


def test_total_taxes(analyzer):
    assert analyzer.total_taxes == pytest.approx(63506.77, abs=1)


def test_net_cash_from_sale(analyzer):
    assert analyzer.net_cash_from_sale == pytest.approx(509_789.92, abs=1)


def test_net_cash_flows(analyzer):
    true_cash_flows = [-337387.5, 63812.22, 67700.56, 71705.56, 75830.70, 589869.52]
    cash_flows = analyzer.investor_waterfall['net_cash_flows']
    assert cash_flows == pytest.approx(true_cash_flows, abs=1)


def test_deal_irr(analyzer):
    assert analyzer.investor_waterfall['deal_irr'] == pytest.approx(0.2675, abs=0.001)


def test_investor_cash_flows(analyzer):
    true_investor_cash_flows = [-303648.75, 42702.51, 44646.68, 46649.18, 48711.75, 440686.16]
    investor_cash_flows = analyzer.investor_waterfall['investor']['cash_flows']
    assert investor_cash_flows == pytest.approx(true_investor_cash_flows, abs=1)


def test_investor_irr(analyzer):
    assert analyzer.investor_waterfall['investor']['irr'] == pytest.approx(0.1904, abs=0.001)


def test_sponsor_irr(analyzer):
    assert analyzer.investor_waterfall['sponsor']['irr'] == pytest.approx(0.7976, abs=0.001)
