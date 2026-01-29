from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    name: str
    text: Optional[str] = None
    title: Optional[str] = None
    status: Optional[str] = None
    remarks: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    name: Optional[str] = None
    text: Optional[str] = None
    title: Optional[str] = None
    status: Optional[str] = None
    remarks: Optional[str] = None

class TaskResponse(TaskBase):
    id: int
    date_time: datetime

    class Config:
        from_attributes = True
