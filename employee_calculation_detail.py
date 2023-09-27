from dataclasses import dataclass


@dataclass
class EmployeeCalculationDetail:
    share_price_vest: float
    exchange_rate_for_vest: float
    tax_rate_upper: int
    income_tax_upper: float
    executed_price: float
    brokerage: float
    citi_spot_rate: float
    shares_vested: float
    estimated_stock_cash_value_rmb: float
    estimated_stock_cash_value_euro: float
    shares_sold: float
    shares_delivered: float
    gross_proceeds_euro: float
    net_proceeds_euro: float
    net_sale_proceeds_cny: float
    actual_income_tax: float
    cash_income: float




