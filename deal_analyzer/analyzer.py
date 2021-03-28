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
                 debt_share,
                 interest_rate,
                 term,
                 amortization_period,
                 gross_rent_roll,
                 vacancy_rate,
                 annual_growth,
                 real_estate_tax_rate,
                 income_tax_rate,
                 sell_price,
                 year_held=5,
                 sell_cap_rate=None
                 ):
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
        self.total_cost = None
        self.debt_share = debt_share
        self.mortgage_amount = None
        self.equity_investment = None
        self.interest_rate = interest_rate
        self.term = term
        self.amortization_period = amortization_period
        self.constant_loan_payments = None

        # operate
        self.gross_rent_roll = gross_rent_roll
        self.vacancy_rate = vacancy_rate
        self.annual_growth = annual_growth
        self.real_estate_tax_rate = real_estate_tax_rate
        self.income_tax_rate = income_tax_rate

        # sell
        self.sell_price = sell_price
        self.years_held = year_held
        self.sell_cap_rate = sell_cap_rate

        # derive remaining assumptions
        self.calculate_assumptions()

    def calculate_assumptions(self):
        self.depreciable_base = self.purchase_price - self.land_value
        self.development_cost = self.improvement_cost_per_sf * self.rentable_sf
        self.total_cost = self.purchase_price + self.development_cost
        self.mortgage_amount = self.total_cost * self.debt_share
        self.equity_investment = self.total_cost - self.mortgage_amount
        self.constant_loan_payments = -pmt(
            rate=self.interest_rate/12,
            nper=self.amortization_period*12,
            pv=self.mortgage_amount
        ) * 12 / self.mortgage_amount


