import pytest


def test_first_year_setup(analyzer):
    assert analyzer.gross_rent_roll == 400950
    assert analyzer.vacancy_rate == pytest.approx(0.322737, abs=0.00001)
    assert analyzer.cash_flow_after_financing == pytest.approx(59_996.48, abs=0.01)
