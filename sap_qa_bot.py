import logging
import openai
import json

import calculation_detail_store

logger = logging.getLogger("qa_bot.py")


class SapBot:
    def __init__(self, system_message_file_name: str, calculation_detail_file_name: str, template_file_name: str, llm: openai):
        self.llm = llm
        self.system_message = open(system_message_file_name).read()
        self.calculation_detail_store = calculation_detail_store.InMemoryCalculationDetail(calculation_detail_file_name, template_file_name)
        self.functions = {'get_calculation_detail': self.calculation_detail_store.get_calculation_detail}
        self.dialogueManager = DialogueManager()


    def get_employee_id(self, input: str) -> str:
        prompt = f"""
        The user provides his input delimited by triple quotes. \
        \"\"\" {input} \"\"\" \    
        You will return the employee ID based on the input.
        Your answer will be in a consistent format, following the examples delimited by triple hyphens below . \
        --- 
            input: I am working in SAP, my ID is 1033961 \
            answer: 1033961 \
            input: I am with ID 1032059 \
            answer: 1032059 \
            input: 1033961 \
            answer: 1033961 \
            input: 1032059 \
            answer: 1032059 \    
        --- 
        Please only return employee id. \
        Ensure do NOT provide anything else, such as expressions. \
       """
        messages = [
            {"role": "user", "content": prompt}
        ]
        print(f'messages sent to openai {messages}')
        response = self.llm.ChatCompletion.create(
            engine="gpt-4",
            messages=messages
        )
        response_message_content = response['choices'][0]['message']['content']
        return response_message_content


    def load_calculation_detail_to_system_message(self, question: str) -> str:  
        employee_id_input = self.get_employee_id(question)
        try:   
            if employee_id_input[0].lower() == 'i':  
                employee_id_str = '1' + employee_id_input[1:]  
            employee_id = int(employee_id_str)  
        except ValueError:  
            return f"你输入的员工号: {employee_id_input}是不合法的"  
    
        try:   
            calculation_detail = self.calculation_detail_store.get_calculation_detail(employee_id)  
        except Exception as e:  
            return f"没有查询到员工: {employee_id_input}的move SAP记录"  
 
        self.system_message = self.system_message + '\n' + calculation_detail  
        print(f'system message updated to: {self.system_message}')  
    
        employee_stock_info = self.calculation_detail_store.get_employee_stock_info(employee_id_input, employee_id) 
        print(f'employee_stock_info : {employee_stock_info}')  
        return employee_stock_info 


    def search(self, question: str) -> str:
        self.dialogueManager.add_message('user', question)
        messages = [
            {"role": "system", "content": self.system_message}
        ]
        messages.extend(self.dialogueManager.dialogue_history)
        print(f'messages sent to openai {messages}')
        response = self.llm.ChatCompletion.create(
            engine="gpt-4",
            messages=messages
        )
        response_message_content = response['choices'][0]['message']['content']
        print(f'openai Response: {response_message_content}')
        self.dialogueManager.add_message('assistant', response_message_content)
        return response_message_content


    def searchViaFunctionCall(self, question: str) -> str:
        self.dialogueManager.add_message('user', question)
        messages = [
            {"role": "system", "content": self.system_message}
        ]
        messages.extend(self.dialogueManager.dialogue_history)
        messages.append({'role': 'user', 'content': question})
        functions = [
            {
                "name": "get_calculation_detail",
                "description": "Retrieves moveSAP calculation steps based on the parameters provided, "
                               "this calculation steps will be used to answer employees' payroll related question"
                               "regarding moveSAP stock grant",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {
                            "type": "integer",
                            "description": "sap i-number of the user"
                        }
                    },
                    "required": ["employee_id"]
                }
            }
        ]
        response = openai.ChatCompletion.create(
            engine="gpt-4",
            messages=messages,
            functions=functions,
            function_call="auto",
        )
        response_message = response['choices'][0]['message']
        print(f'First openai Response: {response_message}')
        if 'function_call' in response_message:
            function_call = response_message['function_call']
            function_to_call = self.functions[function_call['name']]
            function_args = json.loads(function_call['arguments'])
            res = function_to_call(**function_args)
            print(f'function_call result {res}')
            self.dialogueManager.add_message('assistant', f'查询到的当前员工收入MoveSap股票的详细计算过程\n{res}')
            self.dialogueManager.add_message('user', '请根据上下文中的moveSAP计算过程回答我之前的问题')
            messages = [
                {"role": "system", "content": self.system_message},
                {"role": "system",
                 "content": "Don't make assumptions about what values to use with functions. "
                            "Ask for clarification if a user request is ambiguous."}
            ]
            messages.extend(self.dialogueManager.dialogue_history)
            response = openai.ChatCompletion.create(
                engine="gpt-4",
                messages=messages
            )
            print('Second openai response: {}'.format(response['choices'][0]['message']))
            if 'content' in response['choices'][0]['message']:
                return response['choices'][0]['message']['content']
            return ''
        response_message_content = response['choices'][0]['message']['content']
        self.dialogueManager.add_message('assistant', response_message_content)
        return response_message_content

class DialogueManager:

    dialogue_history: list

    def __init__(self):
        self.dialogue_history = []

    def add_message(self, role: str, content: str):
        self.dialogue_history = self.dialogue_history[-17:]
        self.dialogue_history.append({"role": role, "content": content})

    def reset_dialogue(self):
        self.dialogue_history = []
