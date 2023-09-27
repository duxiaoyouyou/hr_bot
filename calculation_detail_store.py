import calculation_detail_parser
from employee_calculation_detail import EmployeeCalculationDetail
from calculation_step_generator import generate_calculation_step


class InMemoryCalculationDetail:
    def __init__(self):
        file = open('resources/MoveSAP_0922.xlsx', 'rb')
        self.data_store = calculation_detail_parser.parse_data_as_dict(file=file)

    def get_calculation_detail(self, employee_id: int) -> EmployeeCalculationDetail:
        detail = self.data_store[employee_id]
        return generate_calculation_step(detail)
