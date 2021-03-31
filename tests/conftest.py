import pytest
from deal_analyzer import DealAnalyzer


@pytest.fixture(scope="session")
def analyzer():
    deal_specs = dict(
        purchase_price=895_000,
        land_value=50_000,
        depreciable_life=27.5,
        building_sf=8_800,
        rentable_sf=6_525,
        improvement_cost_per_sf=62,
        closing_costs=50_000,
        debt_share=0.75,
        interest_rate=0.0425,
        term=5,
        amortization_period=25,
        number_of_units=27,
        monthly_school_rent=650,
        daily_summer_rent=100,
        school_year_occupancy_rate=0.95,
        summer_occupancy_rate=0.50,
        operating_expenses_per_unit=8_800 * 10 / 27,
        capital_reserves_per_unit=357.14,
        annual_growth=0.03,
        real_estate_tax_rate=0.12,
        income_tax_rate=0.3960,
        sell_cap_rate=0.10,
        investor_contribution=0.9,
        investor_preferred_return=0.08,
        investor_profit_share=0.5
    )

    analyzer = DealAnalyzer(**deal_specs)
    return analyzer
