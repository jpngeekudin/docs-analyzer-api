
from langchain_huggingface.embeddings.huggingface_endpoint import HuggingFaceEndpointEmbeddings
from langchain.embeddings.base import Embeddings
import os
from dotenv import load_dotenv
import requests

load_dotenv()


class CustomHTTPEmbedding(Embeddings):
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def embed_documents(self, texts):
        embeddings = []
        for text in texts:
            res = requests.post(self.endpoint, json={"input": text})
            data = res.json()
            vector = data["data"][0]["embedding"]
            embeddings.append(vector)
        return embeddings

    def embed_query(self, text):
        res = requests.post(self.endpoint, json={"input": text})
        data = res.json()
        return data["data"][0]["embedding"]

# ebm = HuggingFaceEndpointEmbeddings(
#     model="ebbge-m3",
#     base_url=os.getenv('EMBEDDING_BASE_URL'),
#     api_key=os.getenv('LLM_API_KEY')
# )

custom_embeddings = CustomHTTPEmbedding(endpoint=os.getenv('EMBEDDING_BASE_URL'))
