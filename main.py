import openai
from move_sap_qa_bot import qa_bot
import streamlit as st
import logging
from sap import cf_logging
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("API_KEY")
openai.api_base = os.getenv("API_BASE")
openai.api_type = "azure"
openai.api_version = "2023-03-15-preview"

@st.cache_data
def set_log():
    cf_logging.init()

set_log()

logger = logging.getLogger("main.py")

openai.api_key = "9f32e291dbd248c2b4372647bd937577"
openai.api_base = "https://miles-playground.openai.azure.com"
openai.api_type = "azure"
openai.api_version = "2023-03-15-preview"

bot = qa_bot(openai)
st.title("HR QA Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "prompt_history" not in st.session_state:
    st.session_state.prompt_history = []
with st.chat_message("assistant"):
    st.markdown("你好，我是AI助手Freya，专门回答关于MoveSAP股票相关的问题。")
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
# Accept user input
if prompt := st.chat_input("How can I help you?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        if len(st.session_state.prompt_history) == 0:
            response = bot.ask_by_calculation(prompt)
            query = response["query"]
            response_message = response["response"]

        else:
            response = bot.ask(prompt, message_history=st.session_state.prompt_history[-16:])
            query = prompt
            response_message = response
        st.session_state.messages.append({"role": "assistant", "content": response_message})
        st.session_state.prompt_history.append({"role": "user", "content": query})
        st.session_state.prompt_history.append({"role": "assistant", "content": response_message})
        message_placeholder.markdown(response_message)
    # Add assistant response to chat history

