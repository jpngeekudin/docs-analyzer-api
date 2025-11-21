import tempfile
import shutil
from services.extractor import extract_text_from_file
from db.vectorstore import vectorstore
from fastapi import File
from helpers.text_split import text_split

async def upload_document(file: File):
    # Save file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    # Extract text
    extracted_text = extract_text_from_file(tmp_path)
    if not extracted_text.strip():
        return {"status": "error", "message": "Unable to extract text from document"}
    
    # Store in Chroma
    chunks = text_split(extracted_text, 1000)
    metadatas = list(map(lambda n: {'filename': file.filename}, chunks))
    return vectorstore.add_texts(
        chunks,
        # metadatas=[{"filename": file.filename}]
        metadatas=metadatas
    )
