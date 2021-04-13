import pytest


def test_first_year_setup(analyzer):
    assert analyzer.gross_rent_roll == 400950
    assert analyzer.vacancy_rate == pytest.approx(0.3833, abs=0.0001)
    assert analyzer.cash_flow_after_financing == pytest.approx(63_812.22, abs=0.01)
