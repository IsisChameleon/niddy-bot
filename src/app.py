import streamlit as st
import os
from modules.chathistory import ChatHistory
from modules.layout import Layout
from modules.helpers import load_api_key
from modules.sidebar import Sidebar
from modules.chatbot import Chatbot
from modules.retrievers.faiss import FaissRetriever
from modules.loaders import MyDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

COLLECTION_NAME = 'NDIS_ALL_PDFPLUMBER_TEXTS_1024_256'

def setupChatbot(model, temperature):
    loader = MyDirectoryLoader(dir_path = '../data')
    splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=256)
    search_kwargs = {
        "distance_metric": "cos",
        "fetch_k": 10, 
        "k": 20,
        "maximal_marginal_relevance": True
    }
    newCollection_kwargs = {
        "loader": loader,
        "splitter": splitter
    }
    retriever = FaissRetriever().build(COLLECTION_NAME, search_kwargs, newCollection_kwargs)

    return Chatbot(model, temperature, retriever)

def initConversation():
    history = ChatHistory()
    history.initialize()
    return setupChatbot(st.session_state["model"], st.session_state["temperature"]), history

#Config
st.set_page_config(layout="wide", page_icon="💬", page_title="Niddy, the Ndis Invoicing Helper Bot")

#Title
st.markdown(
    """
    <h2 style='text-align: center;'>Niddy, your NDIS invoicing specialist</h1>
    """,
    unsafe_allow_html=True,)

st.markdown("---")

#Description
st.markdown(
    """ 
    <h5 style='text-align:center;'>I'm Niddy, a chatbot created to help you invoicing for an NDIS participant</h5>  
      
    Don't enter any PII information such as person names, participant numbers, phone numbers, card details in this chat!!!!
    """,
    unsafe_allow_html=True)
st.markdown("---")

# Instantiate the main components
layout, sidebar = Layout(), Sidebar()

user_api_key = load_api_key()
if not user_api_key:
    layout.show_api_key_missing()
else:
    os.environ["OPENAI_API_KEY"] = user_api_key

    # Configure the sidebar
    sidebar.show_options()
    sidebar.about()

    # # Initialize chat history
    history = ChatHistory()
    
    # Initialize the chatbot if first time or the chat history if button clicked
    if st.session_state["reset_chat"] or \
        st.session_state["tweak"] or \
        "chatbot" not in st.session_state:
            
        chatbot, history = initConversation()
        print(chatbot)
        print(history)
        st.session_state["reset_chat"] = False
        st.session_state["tweak"] = False
        st.session_state["chatbot"] = chatbot

    history.display_chat_messages_history()
    
    # Accept user input
    if prompt := st.chat_input("Please ask a question..."):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            assistant_response, references = st.session_state["chatbot"].conversational_chat(prompt)
            message_placeholder.markdown(assistant_response)
            
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})