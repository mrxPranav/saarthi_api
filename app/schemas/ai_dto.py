from pydantic import BaseModel
from typing import Optional
from enum import Enum

class AIRequestType(str, Enum):
    STORY = "story"
    RESEARCH = "research"
    PROJECT = "project"

class AIRequest(BaseModel):
    system_prompt: Optional[str] = "You are a helpful assistant."
    user_prompt: str

class TypedAIRequest(BaseModel):
    type: AIRequestType
    text: str
    prompt: str

class AIResponse(BaseModel):
    response: str
    model: str
