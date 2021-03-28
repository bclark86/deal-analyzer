import pytest


def test_class_project(analyzer):
    assert analyzer.gross_rent_roll == 400950
    assert analyzer.vacancy_rate == pytest.approx(0.22212, abs=0.00001)
