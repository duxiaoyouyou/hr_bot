import logging
import openai

logger = logging.getLogger("qa_bot.py")


class SapBot:
    def __init__(self, system_message: str, llm: openai):
        self.llm = llm
        self.system_message = system_message
        self.dialogueManager = DialogueManager()
    

    def updateSystemMessge(self, system_message):
        self.system_message = system_message

    def search(self, question: str) -> str:
        if("no_calcualtion_detail" in self.system_message):
            return f"没有查询到的员工的股票信息" 
        self.dialogueManager.add_message('user', question)
        messages = [
            {"role": "system", "content": self.system_message}
        ]
        messages.extend(self.dialogueManager.dialogue_history)
        response = self.llm.ChatCompletion.create(
            engine="gpt-4",
            messages=messages
        )
        response_message_content = response['choices'][0]['message']['content']
        #print(f'openai Response: {response_message_content}')
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
        
    
    # def searchViaFunctionCall(self, question: str) -> str:
    #     self.dialogueManager.add_message('user', question)
    #     messages = [
    #         {"role": "system", "content": self.system_message}
    #     ]
    #     messages.extend(self.dialogueManager.dialogue_history)
    #     messages.append({'role': 'user', 'content': question})
    #     functions = [
    #         {
    #             "name": "get_calculation_detail",
    #             "description": "Retrieves moveSAP calculation steps based on the parameters provided, "
    #                            "this calculation steps will be used to answer employees' payroll related question"
    #                            "regarding moveSAP stock grant",
    #             "parameters": {
    #                 "type": "object",
    #                 "properties": {
    #                     "employee_id": {
    #                         "type": "integer",
    #                         "description": "sap i-number of the user"
    #                     }
    #                 },
    #                 "required": ["employee_id"]
    #             }
    #         }
    #     ]
    #     response = openai.ChatCompletion.create(
    #         engine="gpt-4",
    #         messages=messages,
    #         functions=functions,
    #         function_call="auto",
    #     )
    #     response_message = response['choices'][0]['message']
    #     print(f'First openai Response: {response_message}')
    #     if 'function_call' in response_message:
    #         function_call = response_message['function_call']
    #         function_to_call = self.functions[function_call['name']]
    #         function_args = json.loads(function_call['arguments'])
    #         res = function_to_call(**function_args)
    #         print(f'function_call result {res}')
    #         self.dialogueManager.add_message('assistant', f'查询到的当前员工收入MoveSap股票的详细计算过程\n{res}')
    #         self.dialogueManager.add_message('user', '请根据上下文中的moveSAP计算过程回答我之前的问题')
    #         messages = [
    #             {"role": "system", "content": self.system_message},
    #             {"role": "system",
    #              "content": "Don't make assumptions about what values to use with functions. "
    #                         "Ask for clarification if a user request is ambiguous."}
    #         ]
    #         messages.extend(self.dialogueManager.dialogue_history)
    #         response = openai.ChatCompletion.create(
    #             engine="gpt-4",
    #             messages=messages
    #         )
    #         print('Second openai response: {}'.format(response['choices'][0]['message']))
    #         if 'content' in response['choices'][0]['message']:
    #             return response['choices'][0]['message']['content']
    #         return ''
    #     response_message_content = response['choices'][0]['message']['content']
    #     self.dialogueManager.add_message('assistant', response_message_content)
    #     return response_message_content





