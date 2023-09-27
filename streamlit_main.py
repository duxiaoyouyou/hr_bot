import openai
from move_sap_qa_bot import MoveSapBot
import streamlit as st
import logging
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("API_KEY")
openai.api_base = os.getenv("API_BASE")

logger = logging.getLogger("streamlit_main.py")

openai.api_type = "azure"
openai.api_version = "2023-07-01-preview"


st.title("HR QA Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "bot" not in st.session_state:
    st.session_state.bot = MoveSapBot(openai)
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
    bot = st.session_state.bot
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        response = bot.search(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        message_placeholder.markdown(response)

