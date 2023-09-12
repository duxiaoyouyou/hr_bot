class calculator:
    def __init__(self, shares_to_be_vested, vesting_date_exchange_rate, vesting_date_stock_price,
                 actual_income_tax_rate, exchange_rate_on_transfer,
                 max_income_tax_rate=0.45):
        self.shares_to_be_vested = shares_to_be_vested
        self.max_income_tax_rate = max_income_tax_rate
        self.vesting_date_exchange_rate = vesting_date_exchange_rate
        self.actual_income_tax_rate = actual_income_tax_rate
        self.exchange_rate_on_transfer = exchange_rate_on_transfer
        self.vesting_date_stock_price = vesting_date_stock_price
        self.withold_shares_amount_to_sell = 0.0
        self.withold_income_tax_amount_on_sale = 0.0
        self.actual_income_tax_amount = 0.0
        self.cash_amount_to_citi_bank = 0.0
        self.cash_amount_to_be_paid = 0.0

    def __calculate_withhold_shares_amount_to_sell(self):
        self.withold_shares_amount_to_sell = self.shares_to_be_vested * self.max_income_tax_rate

    def __calculate_withhold_income_tax_amount_on_sale(self):
        self.withold_income_tax_amount_on_sale = self.withold_shares_amount_to_sell * self.vesting_date_exchange_rate * \
                                                 self.vesting_date_stock_price

    def __calculate_actual_income_tax_amount(self):
        self.actual_income_tax_amount = self.shares_to_be_vested * self.actual_income_tax_rate * self.vesting_date_exchange_rate * self.vesting_date_stock_price

    def __calculate_cash_amount_to_citi_bank(self):
        self.cash_amount_to_citi_bank = self.exchange_rate_on_transfer * self.withold_shares_amount_to_sell * self.vesting_date_stock_price

    def __calculate_cash_amount_employees_received(self):
        self.cash_amount_to_be_paid = self.cash_amount_to_citi_bank - self.actual_income_tax_amount

    def calculate(self):
        self.__calculate_withhold_shares_amount_to_sell()
        self.__calculate_withhold_income_tax_amount_on_sale()
        self.__calculate_actual_income_tax_amount()
        self.__calculate_cash_amount_to_citi_bank()
        self.__calculate_cash_amount_employees_received()

    def to_calculation_details(self):
        return f'以下是这次Move SAP股票的相关信息计算：\n' \
               f'1.	在德国，SAP公司给员工发放了{self.shares_to_be_vested}股SAP股票。发放的同时，需要对这些股票的价值进行税务处理。\n' \
               f'当前案例：员工一共收到了{self.shares_to_be_vested}股股票。\n' \
               f'2.	由于中国员工的最高税率是{self.max_income_tax_rate*100}%，所以系统会预先卖掉{self.max_income_tax_rate*100}%的股票以抵税，剩下的部分会转入个人账户。 \n' \
               f'当前案例：需要卖掉的股票数量是：{self.shares_to_be_vested}股 * {self.max_income_tax_rate*100}% = {self.withold_shares_amount_to_sell}股。\n' \
               f'3.	当日的股票价格是10欧元，EQUT卖出股票时，欧元对人民币的汇率是{self.vesting_date_exchange_rate}。\n' \
               f'当前案例：卖掉的预估股票总价值是：{self.withold_shares_amount_to_sell}股 * {self.vesting_date_stock_price}欧元/股 * {self.vesting_date_exchange_rate} = {self.withold_income_tax_amount_on_sale}人民币。\n' \
               f'4.	在中国，实际的个人税率是20%，这部分税由SAP公司代缴，员工在收到股票收入后可以抵扣。\n' \
               f'当前案例：实际需要交的税是：{self.shares_to_be_vested}股 * {self.actual_income_tax_rate*100}% * {self.vesting_date_stock_price}欧元/股 * {self.vesting_date_exchange_rate} = {self.actual_income_tax_amount}人民币，由SAP公司代缴。\n' \
               f'5.	当外汇到达中国时，需要经过一个半月的审核才能发放。在此期间，这些资金由Citi Bank保管。Citi Bank收到欧元并且卖出时，汇率是{self.exchange_rate_on_transfer}。\n' \
               f'当前案例：Citi Bank实际保管的金额是：{self.withold_shares_amount_to_sell}股 * {self.vesting_date_stock_price}欧元/股 * {self.exchange_rate_on_transfer} = {self.cash_amount_to_citi_bank}人民币。\n' \
               f'6.	过了审核期之后，保管的金额减去公司提前代缴的税，差额算作利得，以现金方式发给员工。\n' \
               f'当前案例：员工实际收到的金额是：{self.cash_amount_to_citi_bank}人民币 – {self.actual_income_tax_amount}人民币 = {self.cash_amount_to_be_paid}人民币，这个金额会以Cash的方式出现在员工的工资单上。\n'

#
# calculator = calculator(1000, 7, 10, 0.2, 6.9)
# calculator.calculate()
# print(calculator.to_calculation_details())
