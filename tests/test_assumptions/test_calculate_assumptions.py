import pytest


def test_calculate_assumptions(analyzer):
    """
    GIVEN DealAnalyzer with a set of assumptions
    WHEN the calculate_assumptions method is called
    THEN the derived assumptions will then be calculated
    """
    assert analyzer.depreciable_base == 845_000
    assert analyzer.development_cost == 404_550
    assert analyzer.constant_loan_payments == pytest.approx(0.065009, abs=1e-6)
