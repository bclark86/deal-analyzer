import numpy as np
import pandas as pd
import numpy_financial as npf


class DealAnalyzer:
    def __init__(
        self,
        purchase_price,
        land_value,
        depreciable_life,
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
        operating_expenses_per_sf,
        capital_reserves_per_unit,
        annual_growth,
        real_estate_tax_rate,
        income_tax_rate,
        sell_cap_rate,
        years_held,
        investor_contribution=0.9,
        investor_preferred_return=0.08,
        investor_profit_share=0.5,
        school_year_duration=9,
        summer_year_duration=3,
    ):
        # ASSUMPTIONS

        # buy
        self.purchase_price = purchase_price
        self.land_value = land_value
        self.depreciable_life = depreciable_life
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
        self.operating_expenses_per_sf = operating_expenses_per_sf
        self.operating_expenses_per_unit = (
            self.building_sf * self.operating_expenses_per_sf / self.number_of_units
        )
        self.capital_reserves_per_unit = capital_reserves_per_unit
        self.annual_growth = annual_growth
        self.real_estate_tax_rate = real_estate_tax_rate
        self.income_tax_rate = income_tax_rate

        # sell
        self.sell_price = None
        self.years_held = years_held
        self.sell_cap_rate = sell_cap_rate

        # investors
        self.investor_contribution = np.minimum(investor_contribution, 1)
        self.sponsor_contribution = 1 - self.investor_contribution
        self.investor_preferred_return = investor_preferred_return
        self.investor_profit_share = investor_profit_share
        self.sponsor_profit_share = 1 - self.investor_profit_share

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
        self.depreciation_taken = None
        self.net_book_value = None
        self.gain_on_sale = None
        self.total_taxes = None
        self.mortgage_balance = None
        self.net_cash_from_sale = None

        # derive remaining assumptions
        self.calculate_assumptions()
        self.calculate_first_year_setup()
        self.calculate_investor_waterfall()

    def calculate_assumptions(self):
        self.depreciable_base = self.purchase_price - self.land_value
        self.development_cost = self.improvement_cost_per_sf * self.rentable_sf
        self.total_cost = (
            self.purchase_price + self.development_cost + self.closing_costs
        )
        self.mortgage_amount = self.total_cost * self.debt_share
        self.equity_investment = self.total_cost - self.mortgage_amount
        self.constant_loan_payments = (
            -npf.pmt(
                rate=self.interest_rate / 12,
                nper=self.amortization_period * 12,
                pv=self.mortgage_amount,
            )
            * 12
            / self.mortgage_amount
        )

    def calculate_first_year_setup(self):
        self.school_year_rent = (
            self.number_of_units * self.monthly_school_rent * self.school_year_duration
        )
        self.summer_year_rent = (
            self.number_of_units * self.monthly_summer_rent * self.summer_duration
        )
        self.school_year_vacancy_cost = self.school_year_rent * (
            1 - self.school_year_occupancy_rate
        )
        self.summer_vacancy_cost = self.summer_year_rent * (
            1 - self.summer_occupancy_rate
        )
        self.gross_rent_roll = self.school_year_rent + self.summer_year_rent
        self.vacancy_rate = (
            self.school_year_vacancy_cost + self.summer_vacancy_cost
        ) / self.gross_rent_roll
        self.net_rents = (
            self.gross_rent_roll
            - self.summer_vacancy_cost
            - self.school_year_vacancy_cost
        )
        self.real_estate_taxes = self.gross_rent_roll * self.real_estate_tax_rate
        self.operating_expenses = (
            self.operating_expenses_per_unit * self.number_of_units
        )
        self.capital_reserves = self.capital_reserves_per_unit * self.number_of_units
        self.net_operating_income = (
            self.net_rents
            - self.real_estate_taxes
            - self.operating_expenses
            - self.capital_reserves
        )
        self.finance_payments = self.mortgage_amount * self.constant_loan_payments
        self.cash_flow_after_financing = (
            self.net_operating_income - self.finance_payments
        )

    def calculate_investor_waterfall(self):
        net_operating_income_arr = np.repeat(self.net_operating_income, self.years_held)
        for i in range(1, net_operating_income_arr.size):
            net_operating_income_arr[i] = net_operating_income_arr[i] * (
                (1 + self.annual_growth) ** i
            )
        self.investor_waterfall["net_operating_income"] = net_operating_income_arr
        self.sell_price = (
            self.investor_waterfall["net_operating_income"][-1] / self.sell_cap_rate
        )
        self.investor_waterfall["cash_flow_after_financing"] = (
            self.investor_waterfall["net_operating_income"] - self.finance_payments
        )
        self.depreciation_taken = (
            self.depreciable_base / self.depreciable_life
        ) * self.years_held
        self.net_book_value = (
            self.purchase_price
            + (self.capital_reserves * self.years_held)
            + self.development_cost
            - self.depreciation_taken
        )
        self.gain_on_sale = self.sell_price - self.net_book_value
        taxes_at_25pct = self.depreciation_taken * 0.25
        remaining_gain = self.gain_on_sale - self.depreciation_taken
        taxes_at_20pct = remaining_gain * 0.20
        self.total_taxes = taxes_at_25pct + taxes_at_20pct
        cumulative_principle = (
            npf.ppmt(
                rate=self.interest_rate / 12,
                per=np.arange(1, (self.years_held * 12) + 1),
                nper=self.amortization_period * 12,
                pv=self.mortgage_amount,
            ).sum()
            * -1
        )
        self.mortgage_balance = self.mortgage_amount - cumulative_principle
        self.net_cash_from_sale = (
            self.sell_price - self.mortgage_balance - self.total_taxes
        )
        sale_proceed_arr = np.zeros(self.years_held)
        sale_proceed_arr[-1] = self.net_cash_from_sale
        net_cash_arr = (
            self.investor_waterfall["cash_flow_after_financing"] + sale_proceed_arr
        )
        self.investor_waterfall["net_cash_flows"] = np.insert(
            net_cash_arr, 0, -self.equity_investment
        )
        self.investor_waterfall["deal_irr"] = npf.irr(
            self.investor_waterfall["net_cash_flows"]
        )

        # base
        distributions = self.investor_waterfall["net_cash_flows"][1:]

        # investor
        self.investor_waterfall["investor"] = dict()
        self.investor_waterfall["investor"]["contribution"] = (
            self.investor_contribution * self.equity_investment
        )
        self.investor_waterfall["investor"]["preferred_return"] = (
            self.investor_waterfall["investor"]["contribution"]
            * self.investor_preferred_return
        )
        investor_preferred_return_arr = np.repeat(
            self.investor_waterfall["investor"]["preferred_return"], self.years_held
        )
        investor_preferred_return_arr = np.minimum(
            investor_preferred_return_arr,
            self.investor_waterfall["cash_flow_after_financing"]
        )
        cash_flow_after_investor_pr = (
                self.investor_waterfall["cash_flow_after_financing"] - investor_preferred_return_arr
        )
        # sponsor
        self.investor_waterfall["sponsor"] = dict()
        self.investor_waterfall["sponsor"]["contribution"] = (
                self.sponsor_contribution * self.equity_investment
        )
        self.investor_waterfall["sponsor"]["preferred_return"] = (
                self.investor_waterfall["sponsor"]["contribution"]
                * self.investor_preferred_return
        )
        sponsor_preferred_return_arr = np.repeat(
            self.investor_waterfall["sponsor"]["preferred_return"], self.years_held
        )
        sponsor_preferred_return_arr = np.minimum(
            sponsor_preferred_return_arr,
            cash_flow_after_investor_pr
        )
        # investor
        investor_return_of_investment_arr = np.zeros(self.years_held)
        investor_return_of_investment_arr[-1] = self.investor_waterfall["investor"][
            "contribution"
        ]
        # sponsor
        sponsor_return_of_investment_arr = np.zeros(self.years_held)
        sponsor_return_of_investment_arr[-1] = self.investor_waterfall["sponsor"][
            "contribution"
        ]
        remaining_cash_flow_after_investor_pr = (
            distributions
            - investor_preferred_return_arr
            - sponsor_preferred_return_arr
            - investor_return_of_investment_arr
            - sponsor_return_of_investment_arr
        )
        # investor
        investor_share_remaining_cash_flows = (
            remaining_cash_flow_after_investor_pr * self.investor_profit_share
        )
        investor_cash_flows = (
            investor_preferred_return_arr
            + investor_share_remaining_cash_flows
            + investor_return_of_investment_arr
        )
        self.investor_waterfall["investor"]["cash_flows"] = np.insert(
            investor_cash_flows, 0, -self.investor_waterfall["investor"]["contribution"]
        )
        self.investor_waterfall["investor"]["irr"] = npf.irr(
            self.investor_waterfall["investor"]["cash_flows"]
        )
        # sponsor
        sponsor_share_remaining_cash_flows = (
                remaining_cash_flow_after_investor_pr * self.sponsor_profit_share
        )
        sponsor_cash_flows = (
                sponsor_preferred_return_arr
                + sponsor_share_remaining_cash_flows
                + sponsor_return_of_investment_arr
        )
        self.investor_waterfall["sponsor"]["cash_flows"] = np.insert(
            sponsor_cash_flows, 0, -self.investor_waterfall["sponsor"]["contribution"]
        )
        self.investor_waterfall["sponsor"]["irr"] = npf.irr(
            self.investor_waterfall["sponsor"]["cash_flows"]
        )

