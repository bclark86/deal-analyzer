import pytest
from deal_analyzer.analyzer import DealAnalyzer


@pytest.fixture(scope="session")
def analyzer():
    number_of_units = 27
    monthly_school_rent = 650
    monthly_summer_rent = 100 * 30
    school_year_duration = 9
    school_year_occupancy_rate = 0.95
    summer_occupancy_rate = 0.666

    summer_duration = 12 - school_year_duration
    school_year_rent = number_of_units * monthly_school_rent * school_year_duration
    summer_year_rent = number_of_units * monthly_summer_rent * summer_duration

    school_year_vacancy_cost = school_year_rent * (1 - school_year_occupancy_rate)
    summer_vacancy_cost = summer_year_rent * (1 - summer_occupancy_rate)

    gross_rent_roll = school_year_rent + summer_year_rent
    vacancy_rate = (school_year_vacancy_cost + summer_vacancy_cost) / gross_rent_roll

    deal_specs = dict(
        purchase_price=895_000,
        land_value=50_000,
        building_sf=8_800,
        rentable_sf=6_525,
        improvement_cost_per_sf=62,
        debt_share=0.75,
        interest_rate=0.0425,
        term=5,
        amortization_period=25,
        gross_rent_roll=gross_rent_roll,
        vacancy_rate=vacancy_rate,
        annual_growth=0.03,
        real_estate_tax_rate=0.12,
        income_tax_rate=0.3960,
        sell_price=1_869_849.654981
    )

    analyzer = DealAnalyzer(**deal_specs)
    return analyzer

