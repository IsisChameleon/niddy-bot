import streamlit as st
import os

def load_api_key():
    """
    Loads the OpenAI API key 
    """
    user_api_key = st.sidebar.text_input(label="#### Your OpenAI API key 👇", placeholder="sk-...", type="password")
    if user_api_key:
        st.sidebar.success("API key loaded from sidebar", icon="🚀")
        return user_api_key
    
    if st.secrets["OPENAI_API_KEY"] is not None:
        user_api_key = st.secrets["OPENAI_API_KEY"]
        st.sidebar.success("API key loaded from secrets", icon="🚀")
        return user_api_key 
    
    return user_api_key

    

    