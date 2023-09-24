import unittest
from unittest.mock import patch, Mock
from modules.chatbot import Chatbot  
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage,
    Document
)
# https://www.toptal.com/python/an-introduction-to-mocking-in-python

class TestChatbot(unittest.TestCase):

    @patch('modules.chatbot.ChatOpenAI')
    @patch('modules.chatbot.AnswerConversationBufferMemory')
    @patch('modules.chatbot.ConversationalRetrievalChain.from_llm')
    def setUp(self, mock_from_llm, mock_ConversationBufferMemory, mock_ChatOpenAI):
        self.model_name = "test_model"
        self.temperature = 0.5
        self.retriever = "test_retriever"
        self.mock_res = {
            'answer': 'test_answer',
            'source_documents': [
                Mock(page_content='content1', metadata={'source': 'source1', 'page': 'page1'}),
                Mock(page_content='content2', metadata={'source': 'source1', 'page': 'page2'}),
            ]
        }
        self.chatbot = Chatbot(self.model_name, self.temperature, self.retriever)

        # self.mock_llm = mock_ChatOpenAI.return_value
        # self.mock_memory = mock_ConversationBufferMemory.return_value
        # self.mock_conversational_qa_chain = mock_from_llm.return_value

        

    @patch('modules.chatbot.ChatOpenAI')
    @patch('modules.chatbot.ConversationalRetrievalChain.from_llm')
    def test_init(self, mock_from_llm, mock_ChatOpenAI):
        
        chatbot = self.chatbot
        self.assertEqual(chatbot.model_name, self.model_name)
        self.assertEqual(chatbot.temperature, self.temperature)
        self.assertEqual(chatbot.retriever, self.retriever)
        mock_ChatOpenAI.assert_called_with(model_name=self.model_name, temperature=self.temperature)
        print(chatbot.llm)

    @patch('modules.chatbot.ChatOpenAI')
    @patch('modules.chatbot.ConversationalRetrievalChain.from_llm')
    def test_process_response(self, mock_from_llm, mock_ChatOpenAI):
        

        chatbot = self.chatbot
        
        answer, source_documents = chatbot.process_response(self.mock_res)
        
        self.assertEqual(answer, 'test_answer')
        self.assertEqual(source_documents, {
            'source1': {
                'page1': 'content: "content1"',
                'page2': 'content: "content2"'
            }
        })

    @patch('modules.chatbot.ChatOpenAI')
    @patch('modules.chatbot.ConversationalRetrievalChain.from_llm')
    @patch('modules.chatbot.ConversationalRetrievalChain')
    def test_conversational_chat(self, mock_conversational_qa_chain, mock_from_llm, mock_ChatOpenAI):
        query = 'User query'
        mock_conversational_qa_chain_instance = Mock()
        mock_conversational_qa_chain_instance.return_value = {
            'question':'User query',
            'chat_history':[
                HumanMessage(content='User query'),
                AIMessage(content='AI response')
            ],
            'answer':'AI response',
            'source_documents': [Document(page_content='page_content1',
                                          metadata={
                                              'source':'doc1.pdf',
                                              'file_path':'../data/doc1/pdf',
                                              'page':11, 
                                              'total_pages':101 ,
                                              'Title':'document1'
                                          }),
                                 Document(page_content='page_content2',
                                          metadata={
                                              'source':'doc1.pdf',
                                              'file_path':'../data/doc1/pdf',
                                              'page':21, 
                                              'total_pages':101 ,
                                              'Title':'document1'
                                          })]                                       
        }
        mock_from_llm.return_value = mock_conversational_qa_chain_instance
        chatbot = Chatbot(self.model_name, self.temperature, self.retriever)

        answer, source_documents = chatbot.conversational_chat(query)
        
        self.assertEqual(answer, 'AI response')
        self.assertEqual(source_documents, {
            'document1': {
                'page11': 'content: "page_content1"',
                'page21': 'content: "page_content2"'
            }})

        self.mock_conversational_qa_chain.assert_called_with({"question": query})

if __name__ == '__main__':
    unittest.main()
