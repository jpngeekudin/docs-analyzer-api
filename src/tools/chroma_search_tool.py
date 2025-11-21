from langchain_community.tools import Tool
from db.vectorstore import vectorstore

def chroma_search(query: str):
    """
    Tool function for agents to read/query data from ChromaDB.
    Uses retriever to fetch the most relevant documents.
    """
    retriever = vectorstore.as_retriever(search_kwargs={'k': 3})
    results = retriever._get_relevant_documents(query)
    formatted = []
    for doc in results:
        formatted.append({
            "content": doc.page_content,
            "metadata": doc.metadata
        })
    return formatted

chroma_search_tool = Tool(
    name="chroma_search",
    func=chroma_search,
    description="Use this tool to search and read relevant documents stored in ChromaDB based on a query string."
)