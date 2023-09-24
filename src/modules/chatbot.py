from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.callbacks import get_openai_callback
from modules.memory import AnswerConversationBufferMemory
from modules.prompts import CombineChainPrompt
import os

# #fix Error: module 'langchain' has no attribute 'verbose'
# import langchain
# langchain.verbose = False

COLLECTION_NAME = 'NDIS_ALL_PDFPLUMBER_TEXTS_1024_256'

class Chatbot:

    def __init__(self, model_name, temperature, retriever):
        self.model_name = model_name
        self.temperature = temperature
        self.retriever = retriever
        
        self.llm = ChatOpenAI(model_name=self.model_name, temperature=self.temperature)
        self.memory = AnswerConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.conversational_qa_chain = ConversationalRetrievalChain.from_llm(
                                                        llm=self.llm, 
                                                        retriever=self.retriever, 
                                                        verbose=True, 
                                                        return_source_documents=True, 
                                                        max_tokens_limit=4097, 
                                                        rephrase_question = True, #
                                                        memory=self.memory, #
                                                        combine_docs_chain_kwargs={'prompt': CombineChainPrompt})

        print(f'Chatbot initialized with {model_name}, temperature {self.temperature} and retriever {self.retriever}')

    @staticmethod
    def process_response(res):
        answer = res["answer"]
        source_documents = {}

        for document in res['source_documents']:
            page_content = document.page_content
            source = document.metadata['source']
            page=1
            if 'page' in document.metadata.keys():
                page =document.metadata['page']
            document_string = f'content: "{page_content}"'
            if source not in source_documents:
                source_documents[source] = {}
            source_documents[source][page] = document_string

        return answer, source_documents

    def conversational_chat(self, query):
        """
        Start a conversational chat with a model via Langchain
        """
        print('LANGCHAIN_TRACING_V2:', os.getenv('LANGCHAIN_TRACING_V2'))
        print('LANGCHAIN_ENDPOINT:', os.getenv('LANGCHAIN_PROJECT'))
        print('LANGCHAIN_PROJECT:', os.getenv('LANGCHAIN_PROJECT'))
        res = self.conversational_qa_chain({"question" : query})
        answer, source_documents = self.process_response(res=res)
        return answer, source_documents


# def count_tokens_chain(chain, query):
#     with get_openai_callback() as cb:
#         result = chain.run(query)
#     return result, cb.total_tokens 