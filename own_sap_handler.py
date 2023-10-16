import logging

import calculation_detail_store_ownsap

logger = logging.getLogger("qa_bot.py")


class OwnSapHandler:
    def __init__(self, system_message_file_name: str, calculation_detail_file_name: str, template_file_name: str):
        self.system_message = open(system_message_file_name).read()
        self.calculation_detail_store = calculation_detail_store_ownsap.InMemoryCalculationDetailOwnSap(calculation_detail_file_name, template_file_name)
       

    def load_calculation_detail_to_system_message(self, employee_id_input: str, employee_id: str) -> str:  
        try:   
            calculation_detail = self.calculation_detail_store.get_calculation_detail(employee_id)
        except Exception as e:  
            calculation_detail = '' 
            employee_stock_info = f"没有查询到员工: {employee_id_input}的own SAP记录, , 请重新输入员工号和股票信息"
            userInputEmployeeId = True  
        else:
            employee_stock_info = self.calculation_detail_store.get_employee_stock_info(employee_id_input, employee_id)   
            userInputEmployeeId = False
         
        self.system_message = self.system_message + '\n' + calculation_detail  
        print(f'system message for move sap updated to: {self.system_message}')  
    
        system_message_stock_info = {
            "system_message": self.system_message, 
            "stock_info": employee_stock_info,
            "userInputEmployeeId": userInputEmployeeId
            } 
        return system_message_stock_info
    