from calculation_detail_parser import parse_data
from calculation_step_generator import generate_calculation_step

id = 1033961
file = open('resources/MoveSAP_0922.xlsx', 'rb')
details = parse_data(file)
print(details)
#
# print(generate_prompt(detail))
