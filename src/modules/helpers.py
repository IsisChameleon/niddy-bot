import streamlit as st
from dotenv import load_dotenv
import os

def load_api_key():
    """
    Loads the OpenAI API key 
    """
    user_api_key = st.sidebar.text_input(label="#### Your OpenAI API key 👇", placeholder="sk-...", type="password")
    if user_api_key:
        st.sidebar.success("API key loaded from sidebar", icon="🚀")
        return user_api_key
    
    load_dotenv(override=True)
    return os.getenv("OPENAI_API_KEY")

    

    