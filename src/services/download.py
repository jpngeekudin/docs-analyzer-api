from db.vectorstore import vectorstore

async def download_document(id: str):
    collection = vectorstore._collection
    doc = collection.get(ids=[id])
    return doc