import calculation_detail_parser
from calculation_step_generator import generate_calculation_step


class InMemoryCalculationDetailOwnSap:
    def __init__(self, calculation_detail_file_name: str, template_file_name: str):
        self.calculation_detail_file_name = calculation_detail_file_name
        self.template_file_name = template_file_name
        file = open(calculation_detail_file_name, 'rb')
        self.data_store = calculation_detail_parser.parse_data_as_dict_ownsap(file=file)


    def get_calculation_detail(self, employee_id: str) -> str:
        detail = self.data_store[employee_id]
        return generate_calculation_step(self.template_file_name, detail)
    
    
    def get_employee_stock_info(self, employee_id_input: str, employee_id: str) -> str:  
        detail = self.data_store[employee_id]    
        return f"查询到员工{employee_id_input}在{detail.execution_date}卖出了{detail.shares_sold}份own SAP股票，计算过程已经理解完成。"  
  