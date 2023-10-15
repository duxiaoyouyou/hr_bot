import calculation_detail_parser
from calculation_step_generator import generate_calculation_step


class InMemoryCalculationDetailMoveSap:
    def __init__(self, calculation_detail_file_name: str, template_file_name: str):
        self.calculation_detail_file_name = calculation_detail_file_name
        self.template_file_name = template_file_name
        file = open(calculation_detail_file_name, 'rb')
        self.data_store = calculation_detail_parser.parse_data_as_dict_movesap(file=file)


    def get_calculation_detail(self, employee_id: int) -> str:
        detail = self.data_store[employee_id]
        return generate_calculation_step(self.template_file_name, detail)
    
    
    def get_employee_stock_info(self, employee_id_input: str, employee_id: int) -> str:  
        detail = self.data_store[employee_id]    
        return f"查询到员工{employee_id_input}在{detail.vest_date}获得{detail.shares_vested}份move SAP股票，计算过程已经理解完成。"  
  