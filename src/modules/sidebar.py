import streamlit as st

class Sidebar:

    MODEL_OPTIONS = ["gpt-3.5-turbo-16k", "gpt-4"]
    TEMPERATURE_MIN_VALUE = 0.0
    TEMPERATURE_MAX_VALUE = 1.0
    TEMPERATURE_DEFAULT_VALUE = 0.0
    TEMPERATURE_STEP = 0.01

    @staticmethod
    def about():
        about = st.sidebar.expander("About Niddy 🤖")
        sections = [
            "#### Niddy is an AI chatbot with a conversational memory, designed to help providers invoicing the NDIS.",
            "#### Powered by [Langchain](https://github.com/hwchase17/langchain), [OpenAI](https://platform.openai.com/docs/models/gpt-3-5) and [Streamlit](https://github.com/streamlit/streamlit) ⚡",
            "#### Source code: [isisChameleon/Niddy Bot](https://github.com/IsisChameleon)",
        ]
        for section in sections:
            about.write(section)

    @staticmethod
    def reset_chat_button():
        if st.button("Reset chat"):
            st.session_state["reset_chat"] = True
        st.session_state.setdefault("reset_chat", False)
        
    @staticmethod
    def on_model_parameters_change_callback():
        st.session_state["tweak"] = True

    def model_selector(self):
        model = st.selectbox(label="Model", 
                             options=self.MODEL_OPTIONS, 
                             on_change=self.on_model_parameters_change_callback)
        st.session_state["model"] = model

    def temperature_slider(self):
        temperature = st.slider(
            label="Temperature",
            min_value=self.TEMPERATURE_MIN_VALUE,
            max_value=self.TEMPERATURE_MAX_VALUE,
            value=self.TEMPERATURE_DEFAULT_VALUE,
            step=self.TEMPERATURE_STEP,
            on_change=self.on_model_parameters_change_callback
        )
        st.session_state["temperature"] = temperature
        
    def show_options(self):
        if "tweak" not in st.session_state:
            st.session_state.tweak = False
        with st.sidebar.expander("⚙️ Tweak Niddy", expanded=False):

            self.reset_chat_button()
            self.model_selector()
            self.temperature_slider()
            st.session_state.setdefault("model", self.MODEL_OPTIONS[0])
            st.session_state.setdefault("temperature", self.TEMPERATURE_DEFAULT_VALUE)

    #Contact
    @staticmethod
    def show_contact():
        
        with st.sidebar.expander("📧 Contact"):

            st.write("**GitHub:** [IsisChameleon](https://github.com/IsisChameleon/niddy-bot)")
            st.write("**Hashnode** [Isabelle](https://isabelle.hashnode.dev)")
            st.write("**Mail** : isisdesade@gmail.com")
            
            #Contributing
            st.markdown("### 🌟 Contributing")
            st.markdown("""
            Niddy is under regular development. Feel free to contribute and help me make it even more helpful!
            """)