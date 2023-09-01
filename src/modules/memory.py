# https://github.com/sebaxzero/Juridia/blob/main/PDF%20langchain%20example.ipynb
from langchain.memory import ConversationBufferMemory
from typing import Any, Dict

class AnswerConversationBufferMemory(ConversationBufferMemory):
    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        return super(AnswerConversationBufferMemory, self).save_context(inputs,{'response': outputs['answer']})
    
