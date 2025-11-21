from fastapi import FastAPI, File, UploadFile
import uvicorn
from models.chat import ChatRequest, ChatResponse
from dotenv import load_dotenv
from datetime import datetime
from db.mongo import history_collection
from services.llm_client import llm
from services.upload import upload_document
from services.download import download_document
from services.rag import rag_answer
import time

load_dotenv()

app = FastAPI()

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    ids = await upload_document(file)
    return {"status": "success", "message": "Document uploaded & indexed", "data": ids}

@app.post('/index')
def index():
    return True

@app.post('/chat')
async def chat(request: ChatRequest):
    # prompt = f'''
    # system prompt:
    # Jawablah berdasarkan document document yang sudah di upload ke chromadb menggunakan tools "chroma_search".

    # user prompt:
    # {request.message}
    # '''
    # reply = llm.generate(prompt)

    reply = rag_answer(request.message, doc_ids=request.doc_id)

    # store history to mongodb
    # history_doc = {
    #     "user_id": request.user_id,
    #     "user_message": request.message,
    #     "assistant_response": reply,
    #     "timestamp": datetime.now()
    # }
    # result = await history_collection.insert_one(history_doc)

    created_at = round(time.time() * 1000)

    return ChatResponse(
        response=reply,
        # message_id=str(result.inserted_id)
        message_id="null",
        created_at=created_at
)

@app.get('/docs/{id}')
async def docs(id: str):

    data = await download_document(id)
    return {'data': data}



if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=3000, reload=True)