import streamlit as st
import os

def load_api_key():
    """
    Loads the OpenAI API key from the .env file or 
    from the user's input and returns it
    """
    if not hasattr(st.session_state, "api_key"):
        st.session_state.api_key = None
        
    #you can define your API key in .env directly
    if os.path.exists(".env") and os.environ.get("OPENAI_API_KEY") is not None:
        user_api_key = os.environ["OPENAI_API_KEY"]
        st.sidebar.success("API key loaded from .env", icon="🚀")
    else:
        if st.session_state.api_key is not None:
            user_api_key = st.session_state.api_key
            st.sidebar.success("API key loaded from previous input", icon="🚀")
        else:
            user_api_key = st.sidebar.text_input(
                label="#### Your OpenAI API key 👇", placeholder="sk-...", type="password"
            )
            if user_api_key:
                st.session_state.api_key = user_api_key

    return user_api_key