from langchain_chroma import Chroma
import chromadb
from services.embedder import custom_embeddings

chroma_client = chromadb.HttpClient(host='localhost', port=8000, ssl=False)
vectorstore = Chroma(
    collection_name="documents",
    embedding_function=custom_embeddings,
    client=chroma_client
)

retriever = vectorstore.as_retriever(search_kwargs={'k': 3})