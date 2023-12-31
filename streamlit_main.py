import openai
import re

import streamlit as st
import logging

from dotenv import load_dotenv

from move_sap_handler import MoveSapHandler
from own_sap_handler import OwnSapHandler
from sap_qa_bot import SapBot

load_dotenv('.env')

logger = logging.getLogger("streamlit_main.py")


openai.api_key = "9f32e291dbd248c2b4372647bd937577" #os.getenv("API_KEY")
openai.api_base = "https://miles-playground.openai.azure.com" #os.getenv("API_BASE")W
openai.api_type = "azure"
openai.api_version = "2023-07-01-preview"


def get_employee_id(input: str, llm: openai) -> str:  
        words = input.split()  
        if len(words) == 1 and re.match("^[A-Za-z]*$", words[0]):  
            return words[0]
        
        prompt = f"""
        The user provides his input delimited by triple quotes. \
        \"\"\" {input} \"\"\" \    
        You will return the employee ID.
        Your answer will be in a consistent format, following the examples delimited by triple hyphens below . \
        --- 
            input: I am working in SAP, my ID is i033961 \
            i033961 \
            input: I am with ID i518639 \
            i518639 \  
        --- 
        Please only return employee id. \
        Ensure do NOT provide anything else, such as expressions. \
       """
        messages = [ {"role": "user", "content": prompt} ]
        response = llm.ChatCompletion.create(
            engine="gpt-4",
            messages=messages,
            temperature=0.01
        )
        response_message_content = response['choices'][0]['message']['content']
        print("employee id extracted: " + response_message_content)
        return response_message_content.replace('"','')[:7]


st.title("Welcome to HR QA Bot ^O^")
    
    
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "moveSapbot" not in st.session_state:
    st.session_state.moveSapHandler = MoveSapHandler('resources/movesap_bot_system_message.txt', 'resources/MoveSAP_0922.xlsx',  'movesap.jinga2')
if "ownSapbot" not in st.session_state:
    st.session_state.ownSapHandler = OwnSapHandler('resources/ownsap_bot_system_message.txt', 'resources/own_sap.xlsx',  'ownsap.jinga2')
if "sapbot" not in st.session_state:
    st.session_state.sapbot = SapBot("", openai)
if "userInputEmployeeId" not in st.session_state:
    st.session_state.userInputEmployeeId = True
if "current_employee_id" not in st.session_state:  
    st.session_state.current_employee_id = None


# Clear chat button  
if st.button('Clear Chat'):  
    st.session_state.messages = []  
    st.session_state.moveSapHandler = MoveSapHandler('resources/movesap_bot_system_message.txt', 'resources/MoveSAP_0922.xlsx',  'movesap.jinga2')
    st.session_state.ownSapHandler = OwnSapHandler('resources/ownsap_bot_system_message.txt', 'resources/own_sap.xlsx',  'ownsap.jinga2')
    st.session_state.sapbot = SapBot("", openai)
    st.session_state.userInputEmployeeId = True
    st.session_state.current_employee_id = None


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
        
    moveSapHandler = st.session_state.moveSapHandler
    ownSapHandler = st.session_state.ownSapHandler
    sapbot = st.session_state.sapbot
    
    if st.session_state.userInputEmployeeId == True:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            employee_id_input = get_employee_id(prompt,openai)
            
            # Check if a new valid employee ID is detected  
            if employee_id_input and (st.session_state.current_employee_id is None or st.session_state.current_employee_id != employee_id_input):  
                # Update current employee ID  
                st.session_state.current_employee_id = employee_id_input
                
            try:   
                if employee_id_input[0].lower() == '1':  
                    employee_id_str = 'I' + employee_id_input[1:]
                employee_id = employee_id_input.upper()
            except ValueError:  
                system_message = "no_calculation_detail"
                stock_info = f"你输入的员工号: {employee_id_input}是不合法的， 请重新输入" 
                st.session_state.userInputEmployeeId == True
            else:
                system_message_stock_info = ownSapHandler.load_calculation_detail_to_system_message(employee_id_input, employee_id)  
                system_message = system_message_stock_info["system_message"]
                stock_info = system_message_stock_info["stock_info"]
                st.session_state.messages.append({"role": "assistant", "content": stock_info})
                st.session_state.userInputEmployeeId = system_message_stock_info["userInputEmployeeId"]
                if(st.session_state.userInputEmployeeId == False):
                    sapbot.updateSystemMessge(system_message)  
                        
                    
            message_placeholder.markdown(stock_info)
            
    else:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            response = sapbot.search(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            message_placeholder.markdown(response)
            


    