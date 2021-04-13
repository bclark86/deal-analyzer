import pytest
from deal_analyzer import DealAnalyzer
from deal_analyzer import generate_deal_specs


@pytest.fixture(scope="session")
def analyzer():
    deal_specs = generate_deal_specs()
    analyzer = DealAnalyzer(**deal_specs)
    return analyzer
