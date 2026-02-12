from src.services.interfaces.LLMProvider import LLMProvider
from langchain_ollama import ChatOllama

class OllamaLLM(LLMProvider):
    def __init__(self, model_name: str = "llama3.2"):
        self.model_name = model_name

    def _get_client(self, streaming: bool = False):
        return ChatOllama(
            model=self.model_name,
            streaming=streaming,
            temperature=0
        )

    def generate(self, messages, streaming=False, config=None):
        client = self._get_client(streaming)
        response = client.invoke(messages, config=config)
        return response.content

    def invoke(self, messages, config=None):
        client = self._get_client(streaming=True)
        return client.invoke(messages, config=config)
        
    def bind_tools(self, tools):
        client = self._get_client()
        return client.bind_tools(tools)