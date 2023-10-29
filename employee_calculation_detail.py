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
    grant_share: float
    estimated_stock_cash_value_rmb: float
    estimated_stock_cash_value_euro: float
    shares_sold: float
    shares_delivered: float
    gross_proceeds_euro: float
    net_proceeds_euro: float
    net_sale_proceeds_cny: float
    actual_income_tax: float
    cash_income: float
    vest_date: str
    grant_date: str
    
@dataclass
class EmployeeCalculationDetailOwnSap:
    execution_date: str
    shares_sold: float
    executed_price: float
    gross_proceeds_euro: float
    fees: float
    net_proceeds_euro: float
    exchange_rate: float
    net_proceeds_cny: float
    vehicle: str
    transaction_no: str
    branch: str
    payment_execution_date: str
    




