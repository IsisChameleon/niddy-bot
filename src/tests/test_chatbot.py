import unittest
from unittest.mock import patch, Mock
from modules.chatbot import Chatbot  
import langchain

# https://www.toptal.com/python/an-introduction-to-mocking-in-python

class TestChatbot(unittest.TestCase):

    @patch('langchain.chat_models.ChatOpenAI')
    @patch('langchain.memory.ConversationBufferMemory')
    @patch('langchain.chains.ConversationalRetrievalChain.from_llm')
    def setUp(self, mock_ConversationalRetrievalChain, mock_ConversationBufferMemory, mock_ChatOpenAI):
        self.model_name = "test_model"
        self.temperature = 0.5
        self.retriever = "test_retriever"

        self.mock_llm = mock_ChatOpenAI.return_value
        self.mock_memory = mock_ConversationBufferMemory.return_value
        self.mock_conversational_qa_chain = mock_ConversationalRetrievalChain.return_value

        

    @patch('modules.chatbot.ChatOpenAI')
    @patch('modules.chatbot.ConversationalRetrievalChain.from_llm')
    def test_init(self, mock_from_llm, mock_ChatOpenAI):
        chatbot = Chatbot(self.model_name, self.temperature, self.retriever)
        self.assertEqual(chatbot.model_name, self.model_name)
        self.assertEqual(chatbot.temperature, self.temperature)
        self.assertEqual(chatbot.retriever, self.retriever)
        mock_ChatOpenAI.assert_called_with(model_name=self.model_name, temperature=self.temperature)
        print(chatbot.llm)

    def test_process_response(self):
        mock_res = {
            'answer': 'test_answer',
            'source_documents': [
                Mock(page_content='content1', metadata={'source': 'source1', 'page': 'page1'}),
                Mock(page_content='content2', metadata={'source': 'source1', 'page': 'page2'}),
            ]
        }

        answer, source_documents = self.chatbot.process_response(mock_res)
        self.assertEqual(answer, 'test_answer')
        self.assertEqual(source_documents, {
            'source1': {
                'page1': 'content: "content1"',
                'page2': 'content: "content2"'
            }
        })

    def test_conversational_chat(self):
        query = 'test_query'
        mock_res = {
            'answer': 'test_answer',
            'source_documents': []
        }
        self.mock_conversational_qa_chain.return_value = mock_res

        answer, source_documents = self.chatbot.conversational_chat(query)
        self.assertEqual(answer, 'test_answer')
        self.assertEqual(source_documents, {})

        self.mock_conversational_qa_chain.assert_called_with({"question": query})

if __name__ == '__main__':
    unittest.main()
