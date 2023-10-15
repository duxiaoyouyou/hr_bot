import logging
import openai
import json

import calculation_detail_store_movesap

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
