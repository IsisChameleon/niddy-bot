import streamlit as st
import os
from io import StringIO
import re
import sys
from modules.chathistory import ChatHistory
from modules.layout import Layout
from modules.helpers import load_api_key
from modules.sidebar import Sidebar
from modules.chatbot import Chatbot
from modules.retriever import ChromaRetriever

COLLECTION_NAME = 'NDIS_ALL_PDFPLUMBER_TEXTS_1024_128'

#Config
st.set_page_config(layout="wide", page_icon="💬", page_title="Niddy, the Ndis Invoicing Helper Bot")


#Contact
with st.sidebar.expander("📧 Contact"):

    st.write("**GitHub:** [IsisChameleon](https://github.com/IsisChameleon)")
    st.write("**Hashnode** [Isabelle](https://isabelle.hashnode.dev)")
    st.write("**Mail** : isisdesade@gmail.com")

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

    # Initialize chat history
    history = ChatHistory()
    try:
        if (st.session_state["retriever"] is None):
            retriever = ChromaRetriever().fromExistingCollection(collection_name='NDIS_ALL_PDFPLUMBER_TEXTS_1024_128')
            st.session_state["retriever"]=retriever
        chatbot = Chatbot(st.session_state["model"], st.session_state["temperature"], retriever)
        
        # if 'chatbot' not in st.session_state:
        #     st.session_state['chatbot'] = None
        st.session_state["chatbot"] = chatbot

        # Create containers for chat responses and user prompts
        response_container, prompt_container = st.container(), st.container()

        with prompt_container:
            # Display the prompt form
            is_ready, user_input = layout.prompt_form()

            # Initialize the chat history
            history.initialize()

            # Reset the chat history if button clicked
            if st.session_state["reset_chat"]:
                history.reset()

            if is_ready:
                # Update the chat history and display the chat messages
                history.append("user", user_input)

                old_stdout = sys.stdout
                sys.stdout = captured_output = StringIO()

                output = st.session_state["chatbot"].conversational_chat(user_input)
                
                st.session_state["history"].append((user_input, output))

                sys.stdout = old_stdout

                history.append("assistant", output)

                # Clean up the agent's thoughts to remove unwanted characters
                thoughts = captured_output.getvalue()
                cleaned_thoughts = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', thoughts)
                cleaned_thoughts = re.sub(r'\[1m>', '', cleaned_thoughts)

                # Display the agent's thoughts
                with st.expander("Display the agent's thoughts"):
                    st.write(cleaned_thoughts)

        history.generate_messages(response_container)
    except Exception as e:
        st.error(f"Error: {str(e)}")

# #Robby's Pages
# st.subheader("🚀 Niddy's Pages")
# st.write("""
# - **Robby-Chat**: General Chat on data (PDF, TXT,CSV) with a [vectorstore](https://github.com/facebookresearch/faiss) (index useful parts(max 4) for respond to the user) | works with [ConversationalRetrievalChain](https://python.langchain.com/en/latest/modules/chains/index_examples/chat_vector_db.html)
# - **Robby-Sheet** (beta): Chat on tabular data (CSV) | for precise information | process the whole file | works with [CSV_Agent](https://python.langchain.com/en/latest/modules/agents/toolkits/examples/csv.html) + [PandasAI](https://github.com/gventuri/pandas-ai) for data manipulation and graph creation
# - **Robby-Youtube**: Summarize YouTube videos with [summarize-chain](https://python.langchain.com/en/latest/modules/chains/index_examples/summarize.html)
# """)
# st.markdown("---")


#Contributing
st.markdown("### 🌟 Contributing")
st.markdown("""
**Niddy is under regular development. Feel free to contribute and help me make it even more helpful!**
""", unsafe_allow_html=True)