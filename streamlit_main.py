import openai

import streamlit as st
import logging
import os
from dotenv import load_dotenv

from move_sap_qa_bot import MoveSapBot
from own_sap_qa_bot import OwnSapBot

load_dotenv('.env')

openai.api_key = "9f32e291dbd248c2b4372647bd937577" #os.getenv("API_KEY")
openai.api_base = "https://miles-playground.openai.azure.com" #os.getenv("API_BASE")W

logger = logging.getLogger("streamlit_main.py")

openai.api_type = "azure"
openai.api_version = "2023-07-01-preview"

def get_employee_id(input: str, llm: openai) -> str:  
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
        response = llm.ChatCompletion.create(
            engine="gpt-4",
            messages=messages
        )
        response_message_content = response['choices'][0]['message']['content']
        return response_message_content



st.title("Welcome to HR QA Bot!")

# Clear chat history button  
if st.button('Clear Chat History'):  
    st.session_state.messages = []  
    st.session_state.moveSapbot = MoveSapBot('resources/movesap_bot_system_message.txt', 'resources/MoveSAP_0922.xlsx',  'movesap.jinga2', openai)
    st.session_state.ownSapbot = OwnSapBot('resources/ownsap_bot_system_message.txt', 'resources/OwnSAP_2022_Nov.xlsx',  'ownsap.jinga2', openai)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "moveSapbot" not in st.session_state:
    st.session_state.moveSapbot = MoveSapBot('resources/movesap_bot_system_message.txt', 'resources/MoveSAP_0922.xlsx',  'movesap.jinga2', openai)
if "ownSapbot" not in st.session_state:
    st.session_state.ownSapbot = OwnSapBot('resources/ownsap_bot_system_message.txt', 'resources/OwnSAP_2022_Nov.xlsx',  'ownsap.jinga2', openai)

with st.chat_message("assistant"):
    st.markdown(open('resources/hello_message.txt', encoding='utf-8').read())  
    
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
  
# Accept user input
if prompt := st.chat_input("How can I help you?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
        
    moveSapbot = st.session_state.moveSapbot
    ownSapbot = st.session_state.ownSapbot
    
    if len(st.session_state.messages) == 0:
        
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            employee_id_input = get_employee_id(prompt,openai)
            response_movesap = moveSapbot.load_calculation_detail_to_system_message(employee_id_input) 
            st.session_state.messages.append({"role": "assistant", "content": response_movesap})
            response_ownsap = ownSapbot.load_calculation_detail_to_system_message(employee_id_input) 
            st.session_state.messages.append({"role": "assistant", "content": response_ownsap})
            response = f"""
                {response_movesap}  ;
                {response_ownsap}
            """   
            message_placeholder.markdown(response)
    else:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            response_movesap = moveSapbot.search(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response_movesap})
            response_ownsap = ownSapbot.search(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response_ownsap})
            response = f"""
                {response_movesap}  \
                {response_ownsap}
            """   
            message_placeholder.markdown(response)
            


