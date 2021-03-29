import numpy as np
import pandas as pd
from numpy_financial import pmt


class DealAnalyzer:
    def __init__(self,
                 purchase_price,
                 land_value,
                 building_sf,
                 rentable_sf,
                 improvement_cost_per_sf,
                 closing_costs,
                 debt_share,
                 interest_rate,
                 term,
                 amortization_period,
                 number_of_units,
                 monthly_school_rent,
                 daily_summer_rent,
                 school_year_occupancy_rate,
                 summer_occupancy_rate,
                 operating_expenses_per_unit,
                 capital_reserves_per_unit,
                 annual_growth,
                 real_estate_tax_rate,
                 income_tax_rate,
                 sell_cap_rate,
                 school_year_duration=9,
                 summer_year_duration=3,
                 year_held=5
                 ):

        # ASSUMPTIONS

        # buy
        self.purchase_price = purchase_price
        self.land_value = land_value
        self.depreciable_base = None

        # develop
        self.building_sf = building_sf
        self.rentable_sf = rentable_sf
        self.improvement_cost_per_sf = improvement_cost_per_sf
        self.development_cost = None

        # finance
        self.closing_costs = closing_costs
        self.total_cost = None
        self.debt_share = debt_share
        self.mortgage_amount = None
        self.equity_investment = None
        self.interest_rate = interest_rate
        self.term = term
        self.amortization_period = amortization_period
        self.constant_loan_payments = None

        # operate
        self.number_of_units = number_of_units
        self.monthly_school_rent = monthly_school_rent
        self.daily_summer_rent = daily_summer_rent
        self.monthly_summer_rent = self.daily_summer_rent * 30
        self.school_year_duration = school_year_duration
        self.school_year_occupancy_rate = school_year_occupancy_rate
        self.summer_occupancy_rate = summer_occupancy_rate
        self.summer_duration = summer_year_duration
        self.operating_expenses_per_unit = operating_expenses_per_unit
        self.capital_reserves_per_unit = capital_reserves_per_unit
        self.annual_growth = annual_growth
        self.real_estate_tax_rate = real_estate_tax_rate
        self.income_tax_rate = income_tax_rate

        # sell
        self.sell_price = None
        self.years_held = year_held
        self.sell_cap_rate = sell_cap_rate

        # first year setup
        self.school_year_rent = None
        self.summer_year_rent = None
        self.gross_rent_roll = None
        self.school_year_vacancy_cost = None
        self.summer_vacancy_cost = None
        self.vacancy_rate = None
        self.net_rents = None
        self.real_estate_taxes = None
        self.operating_expenses = None
        self.capital_reserves = None
        self.net_operating_income = None
        self.finance_payments = None
        self.cash_flow_after_financing = None

        # investor waterfall
        self.investor_waterfall = dict()

        # derive remaining assumptions
        self.calculate_assumptions()
        self.calculate_first_year_setup()
        self.calculate_investor_waterfall()

    def calculate_assumptions(self):
        self.depreciable_base = self.purchase_price - self.land_value
        self.development_cost = self.improvement_cost_per_sf * self.rentable_sf
        self.total_cost = self.purchase_price \
            + self.development_cost \
            + self.closing_costs
        self.mortgage_amount = self.total_cost * self.debt_share
        self.equity_investment = self.total_cost - self.mortgage_amount
        self.constant_loan_payments = -pmt(
            rate=self.interest_rate/12,
            nper=self.amortization_period*12,
            pv=self.mortgage_amount
        ) * 12 / self.mortgage_amount

    def calculate_first_year_setup(self):
        self.school_year_rent = self.number_of_units \
            * self.monthly_school_rent \
            * self.school_year_duration
        self.summer_year_rent = self.number_of_units \
            * self.monthly_summer_rent \
            * self.summer_duration
        self.school_year_vacancy_cost = self.school_year_rent \
            * (1 - self.school_year_occupancy_rate)
        self.summer_vacancy_cost = self.summer_year_rent \
            * (1 - self.summer_occupancy_rate)
        self.gross_rent_roll = self.school_year_rent + self.summer_year_rent
        self.vacancy_rate = (self.school_year_vacancy_cost + self.summer_vacancy_cost) \
            / self.gross_rent_roll
        self.net_rents = self.gross_rent_roll\
            - self.summer_vacancy_cost\
            - self.school_year_vacancy_cost
        self.real_estate_taxes = self.gross_rent_roll * self.real_estate_tax_rate
        self.operating_expenses = self.operating_expenses_per_unit * self.number_of_units
        self.capital_reserves = self.capital_reserves_per_unit * self.number_of_units
        self.net_operating_income = self.net_rents \
            - self.real_estate_taxes \
            - self.operating_expenses \
            - self.capital_reserves
        self.finance_payments = self.mortgage_amount * self.constant_loan_payments
        self.cash_flow_after_financing = self.net_operating_income - self.finance_payments

    def calculate_investor_waterfall(self):
        net_operating_income_arr = np.repeat(self.net_operating_income, self.years_held)
        for i in range(1, net_operating_income_arr.size):
            net_operating_income_arr[i] = net_operating_income_arr[i] * ((1+self.annual_growth) ** i)
        self.investor_waterfall['net_operating_income'] = net_operating_income_arr
        self.sell_price = self.investor_waterfall['net_operating_income'][-1] / self.sell_cap_rate


