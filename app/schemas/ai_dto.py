from pydantic import BaseModel
from typing import Optional

class AIRequest(BaseModel):
    role: str = "user"
    content: str

class AIResponse(BaseModel):
    response: str
    model: str
