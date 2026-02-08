import os
from src.services.interfaces.LLMProvider import LLMProvider
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

class GeminiLLM(LLMProvider):
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self.model_name = model_name
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key: raise ValueError("Missing GOOGLE_API_KEY")

    def _get_client(self, streaming: bool = False):
        return ChatGoogleGenerativeAI(
            model=self.model_name,
            google_api_key=self.api_key,
            streaming=streaming
        )

    def generate(self, messages, streaming=False, config=None):
        client = self._get_client(streaming)
        response = client.invoke(messages, config=config)
        return response.content

    def invoke(self, messages, config=None):
        client = self._get_client(streaming=False)
        return client.invoke(messages, config=config)
        
    def bind_tools(self, tools):
        client = self._get_client()
        return client.bind_tools(tools)