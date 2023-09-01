from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.callbacks import get_openai_callback
from modules.memory import AnswerConversationBufferMemory
from modules.retriever import ChromaRetriever
from modules.prompts import CombineChainPrompt
from dotenv import load_dotenv

# #fix Error: module 'langchain' has no attribute 'verbose'
# import langchain
# langchain.verbose = False

COLLECTION_NAME = 'NDIS_ALL_PDFPLUMBER_TEXTS_1024_128'

class Chatbot:

    def __init__(self, model_name, temperature, retriever):
        self.model_name = model_name
        self.temperature = temperature
        self.retriever = retriever

        print(f'Chatbot initialized with {model_name}, temperature {self.temperature} and retriever {self.retriever}')

    @staticmethod
    def process_response(res):
        answer = res["answer"]
        source_documents = {}

        for document in res['source_documents']:
            page_content = document.page_content
            source = document.metadata['source']
            page = document.metadata['page']
            document_string = f'content: "{page_content}"'
            if source not in source_documents:
                source_documents[source] = {}
            source_documents[source][page] = document_string

        return answer, source_documents

    def send_query(self, prompt: str, chain):
        res = chain({"question" : prompt})
        answer, source_documents = self.process_response(res=res)
        return answer, source_documents

    def conversational_chat(self, query):
        """
        Start a conversational chat with a model via Langchain
        """
        llm = ChatOpenAI(model_name=self.model_name, temperature=self.temperature)
        memory = AnswerConversationBufferMemory(memory_key="chat_history", return_messages=True)
        conversational_qa_chain = ConversationalRetrievalChain.from_llm(
                                                        llm=llm, 
                                                        retriever=self.retriever, 
                                                        verbose=True, 
                                                        return_source_documents=True, 
                                                        max_tokens_limit=4097, 
                                                        rephrase_question = True, #
                                                        memory=memory, #
                                                        combine_docs_chain_kwargs={'prompt': CombineChainPrompt})

        # chain_input = {"question": query, "chat_history": st.session_state["history"]}
        # result = conversational_qa_chain(chain_input)
        answer, source_documents = self.send_query(prompt=query, chain=conversational_qa_chain)

        #count_tokens_chain(chain, chain_input)
        return answer


def count_tokens_chain(chain, query):
    with get_openai_callback() as cb:
        result = chain.run(query)
    return result, cb.total_tokens 