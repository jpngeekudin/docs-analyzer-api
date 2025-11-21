from db.vectorstore import vectorstore
from langchain_core.prompts.chat import ChatPromptTemplate
from services.llm_client import llm
from typing import List

def rag_answer(query: str, doc_ids: List[str]):
    # retriever = vectorstore.as_retriever(search_kwargs={'k': 3})
    # docs = retriever.invoke(query)
    docs = []

    print(doc_ids)
    
    if doc_ids is not None and len(doc_ids) > 0:
        docs = vectorstore.get_by_ids(doc_ids)

    context = "\n".join([d.page_content for d in docs])
    prompt = ChatPromptTemplate.from_messages([
        ('system', 'You are an AI assistant that answers using provided context.'),
        ('human', f"Context: {context}"),
        ('user', query)
    ])
    formatted = prompt.format_messages(context=context, query=query)
    return llm.generate_from_formatted_prompt(formatted)
    # print(formatted)
    # return ''