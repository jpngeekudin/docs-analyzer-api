# base_llm_client.py

from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage
from tools.chroma_search_tool import chroma_search_tool
from dotenv import load_dotenv
import os

load_dotenv()

class BaseLLMClient:
    def __init__(self, base_url: str, api_key: str, model_name: str = "gpt-oss-20b"):
        self.client = ChatOpenAI(
            base_url=base_url,
            api_key=api_key,
            model=model_name,
            temperature=0.2
        )

        self.client.bind_tools([chroma_search_tool], strict=True)

    def generate(self, prompt: str) -> str:
        response = self.client.invoke([HumanMessage(content=prompt)])
        print(response.tool_calls)
        return response.content
    
    def generate_from_formatted_prompt(self, formatted: any) -> str:
        response = self.client.invoke(formatted)
        return response.content

# Example usage (to be removed or commented out if used as a module)
# if __name__ == "__main__":
#     llm = BaseLLMClient(
#         base_url="http://localhost:8000/v1",
#         api_key="dummy-key",
#         model_name="gpt-oss-20b"
#     )
#     print(llm.generate("Hello, what can you do?"))


llm = BaseLLMClient(
    base_url=os.getenv('LLM_BASE_URL'),
    api_key=os.getenv('LLM_API_KEY'),
    model_name="gpt-oss-20b"
)