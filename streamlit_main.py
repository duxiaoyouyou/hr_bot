import openai
from sap_qa_bot import SapBot
import streamlit as st
import logging
import os
from dotenv import load_dotenv

load_dotenv('.env')

openai.api_key = "9f32e291dbd248c2b4372647bd937577" #os.getenv("API_KEY")
openai.api_base = "https://miles-playground.openai.azure.com" #os.getenv("API_BASE")W

logger = logging.getLogger("streamlit_main.py")

openai.api_type = "azure"
openai.api_version = "2023-07-01-preview"


st.title("Welcome to HR QA Bot!")

# Clear chat history button  
if st.button('Clear Chat History'):  
    st.session_state.messages = []  
    
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "moveSapbot" not in st.session_state:
    st.session_state.moveSapbot = SapBot('resources/movesap_bot_system_message.txt', 'resources/MoveSAP_0922.xlsx',  'movesap.jinga2', openai)
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
    if len(st.session_state.messages) == 0:
        
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            response = moveSapbot.load_calculation_detail_to_system_message(prompt) #"查询计算过程已完成"
            st.session_state.messages.append({"role": "assistant", "content": response})
            message_placeholder.markdown(response)
    else:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            response = moveSapbot.search(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            message_placeholder.markdown(response)


