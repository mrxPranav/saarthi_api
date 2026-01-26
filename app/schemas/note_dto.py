from pydantic import BaseModel
from typing import Optional
from datetime import datetime as dt

class NoteBase(BaseModel):
    note: str
    category: Optional[str] = None
    sub_category: Optional[str] = None
    status: Optional[str] = None
    remark: Optional[str] = None

class NoteCreate(NoteBase):
    pass

class NoteUpdate(NoteBase):
    pass

class NoteResponse(NoteBase):
    id: int
    datetime: Optional[dt] = None

    class Config:
        from_attributes = True
