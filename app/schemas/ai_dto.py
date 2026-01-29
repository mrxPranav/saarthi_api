from pydantic import BaseModel
from typing import Optional

class AIRequest(BaseModel):
    system_prompt: Optional[str] = "You are a helpful assistant."
    user_prompt: str

class AIResponse(BaseModel):
    response: str
    model: str
