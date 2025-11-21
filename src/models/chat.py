from pydantic import BaseModel, Field
from typing import Optional, List

class ChatRequest(BaseModel):
    user_id: str
    message: str
    doc_id: Optional[List[str]] = None


class ChatResponse(BaseModel):
    response: str
    message_id: str
    created_at: int