from employee_calculation_detail import EmployeeCalculationDetail, EmployeeCalculationDetailOwnSap
import pandas as pd
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta

logger = logging.getLogger("calculation_detail_parser.logger")


def parse_data(file, employee_id: int) -> EmployeeCalculationDetail:
    df_9m70 = pd.read_excel(file, sheet_name='9M70')
    estimated_stock_cash_value_rmb = df_9m70[df_9m70['Personnel Number'] == employee_id]['9M61-Equity shares taxabl.amt.'][0]
    df_indie_ex = pd.read_excel(file, sheet_name='By Indi', nrows=1, header=None)
    citi_spot_exchange_rate = df_indie_ex[12][0]
    df_indie = pd.read_excel(file, sheet_name='By Indi', skiprows=[0, 1])
    df_indie = df_indie[df_indie['ID'] == employee_id]
    net_sale_proceeds_cny = df_indie['Net sale proceeds in CNY(A)'][0]
    actual_income_tax = df_indie['SAP Advance Payment(B)'][0]
    cash_income = df_indie['Remaining Amount in LC to GPT (D)'][0]
    df_report = pd.read_excel(file, sheet_name='Report')
    df_employee_report = df_report[df_report['TAXPAYER_ID_(PERS_NO)'] == employee_id]
    share_price_vest = df_employee_report['SHARE_PRICE_VEST'][0]
    vest_date = datetime.combine(df_employee_report['VEST_DATE'][0].date, datetime.min.time())
    grant_date = vest_date + relativedelta(months=-6)
    exchange_rate_for_vest = df_employee_report['EXCHANGE_RATE_FOR_VEST'][0]
    tax_rate_upper = df_employee_report['TAX_RATE_(USED_TO_CALCULATE_ESTIMATED_STC)'][0]
    executed_price = df_employee_report['EXECUTED_PRICE'][0]
    brokerage = df_employee_report['FEES'][0]
    shares_vested = df_employee_report['SHARES_VESTED'][0]
    estimated_stock_cash_value_euro = df_employee_report['TAXABLE_BENEFIT-WAGETYPE_9M61__9M62/_9M65/_9M66'][0]
    shares_sold = df_employee_report['SHARES_SOLD'][0]
    shares_delivered = df_employee_report['SHARES_DELIVERED'][0]
    gross_proceeds_euro = df_employee_report['GROSS_PROCEEDS'][0]
    net_proceeds_euro = df_employee_report['NET_PROCEEDS_9M64'][0]
    return EmployeeCalculationDetail(share_price_vest=share_price_vest,
                                     exchange_rate_for_vest=exchange_rate_for_vest,
                                     tax_rate_upper=tax_rate_upper,
                                     income_tax_upper=round(estimated_stock_cash_value_euro * tax_rate_upper / 100, 2),
                                     executed_price=executed_price,
                                     brokerage=brokerage,
                                     citi_spot_rate=citi_spot_exchange_rate,
                                     shares_vested=shares_vested,
                                     grant_share = round(shares_vested * 6),
                                     estimated_stock_cash_value_rmb=estimated_stock_cash_value_rmb,
                                     estimated_stock_cash_value_euro=estimated_stock_cash_value_euro,
                                     shares_sold=shares_sold,
                                     shares_delivered=shares_delivered,
                                     gross_proceeds_euro=gross_proceeds_euro,
                                     net_proceeds_euro=net_proceeds_euro,
                                     net_sale_proceeds_cny=net_sale_proceeds_cny,
                                     actual_income_tax=actual_income_tax,
                                     cash_income=cash_income,
                                     grant_date=grant_date.strftime('%Y/%m/%d'),
                                     vest_date=vest_date.strftime('%Y/%m/%d'))


def parse_data_as_dict_movesap(file) -> dict[int, EmployeeCalculationDetail]:
    employee_id_vs_calculation_detail = {}
    df_indie_ex = pd.read_excel(file, sheet_name='By Indi', nrows=1, header=None)
    citi_spot_exchange_rate = df_indie_ex[12][0]

    df_report = pd.read_excel(file, sheet_name='Report')
    employee_ids = df_report['TAXPAYER_ID_(PERS_NO)'].tolist()
    for employee_id in employee_ids:
        df_employee_report = df_report[df_report['TAXPAYER_ID_(PERS_NO)'] == employee_id]
        share_price_vest = df_employee_report['SHARE_PRICE_VEST'][0]
        exchange_rate_for_vest = df_employee_report['EXCHANGE_RATE_FOR_VEST'][0]
        tax_rate_upper = df_employee_report['TAX_RATE_(USED_TO_CALCULATE_ESTIMATED_STC)'][0]
        executed_price = df_employee_report['EXECUTED_PRICE'][0]
        brokerage = df_employee_report['FEES'][0]
        shares_vested = df_employee_report['SHARES_VESTED'][0]
        estimated_stock_cash_value_euro = df_employee_report['TAXABLE_BENEFIT-WAGETYPE_9M61__9M62/_9M65/_9M66'][0]
        shares_sold = df_employee_report['SHARES_SOLD'][0]
        shares_delivered = df_employee_report['SHARES_DELIVERED'][0]
        gross_proceeds_euro = df_employee_report['GROSS_PROCEEDS'][0]
        net_proceeds_euro = df_employee_report['NET_PROCEEDS_9M64'][0]
        vest_date = pd.to_datetime(df_employee_report['VEST_DATE'][0])
        # vest_date = datetime.strptime(df_employee_report['VEST_DATE'][0], '%Y/%m/%d')
        grant_date = vest_date + relativedelta(months=-6)
        df_indie = pd.read_excel(file, sheet_name='By Indi', skiprows=[0, 1])
        df_indie = df_indie[df_indie['ID'] == employee_id]
        net_sale_proceeds_cny = df_indie['Net sale proceeds in CNY(A)'][0]
        actual_income_tax = df_indie['SAP Advance Payment(B)'][0]
        cash_income = df_indie['Remaining Amount in LC to GPT (D)'][0]
        df_9m70 = pd.read_excel(file, sheet_name='9M70')
        estimated_stock_cash_value_rmb = df_9m70[df_9m70['Personnel Number'] == employee_id]['9M61-Equity shares taxabl.amt.'][0]
        employee_id_vs_calculation_detail[employee_id] = EmployeeCalculationDetail(share_price_vest=share_price_vest,
                                                                                   exchange_rate_for_vest=exchange_rate_for_vest,
                                                                                   tax_rate_upper=tax_rate_upper,
                                                                                   income_tax_upper=round(
                                                                                       estimated_stock_cash_value_euro * tax_rate_upper / 100,
                                                                                       2),
                                                                                   executed_price=executed_price,
                                                                                   brokerage=brokerage,
                                                                                   citi_spot_rate=citi_spot_exchange_rate,
                                                                                   shares_vested=shares_vested,
                                                                                   grant_share = round(shares_vested * 6),
                                                                                   estimated_stock_cash_value_rmb=estimated_stock_cash_value_rmb,
                                                                                   estimated_stock_cash_value_euro=estimated_stock_cash_value_euro,
                                                                                   shares_sold=shares_sold,
                                                                                   shares_delivered=shares_delivered,
                                                                                   gross_proceeds_euro=gross_proceeds_euro,
                                                                                   net_proceeds_euro=net_proceeds_euro,
                                                                                   net_sale_proceeds_cny=net_sale_proceeds_cny,
                                                                                   actual_income_tax=actual_income_tax,
                                                                                   vest_date=vest_date.strftime('%Y/%m/%d'),
                                                                                   grant_date=grant_date.strftime('%Y/%m/%d'),
                                                                                   cash_income=cash_income)
    return employee_id_vs_calculation_detail


def parse_data_as_dict_ownsap(file) -> dict[int, EmployeeCalculationDetailOwnSap]:
    employee_id_vs_calculation_detail = {}
    df_indie_ex = pd.read_excel(file, sheet_name='By Indi', nrows=3, header=None)
    exchange_rate = df_indie_ex[8][2]
    
    df_report = pd.read_excel(file, sheet_name='Print')
    employee_ids = df_report['SSO_ID'].tolist()
    for employee_id in employee_ids:
        df_employee_report = df_report[df_report['SSO_ID'] == employee_id]
        execution_date = pd.to_datetime(df_employee_report['EXECUTION_DATE'][0])
        shares_sold = df_employee_report['SHARES_SOLD'][0]
        executed_price = df_employee_report['EXECUTED_PRICE'][0]
        gross_proceeds_euro=executed_price * shares_sold                                                                                  
        fees = df_employee_report['FEES'][0]
        net_proceeds_euro=gross_proceeds_euro - fees
        net_proceeds_cny=net_proceeds_euro * exchange_rate                      
        employee_id_vs_calculation_detail[employee_id] = EmployeeCalculationDetailOwnSap(execution_date=execution_date.strftime('%Y/%m/%d'),
                                                                                   shares_sold=shares_sold,
                                                                                   executed_price=executed_price,
                                                                                   gross_proceeds_euro=gross_proceeds_euro,
                                                                                   fees = fees,
                                                                                   net_proceeds_euro=net_proceeds_euro,
                                                                                   exchange_rate=exchange_rate,
                                                                                   net_proceeds_cny=net_proceeds_cny)
    return employee_id_vs_calculation_detail
