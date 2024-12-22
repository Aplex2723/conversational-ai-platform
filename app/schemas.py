from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MessageCreate(BaseModel):
    content: str

class MessageResponse(BaseModel):
    id: int
    is_ai: bool
    content: str
    timestamp: datetime

    class Config:
        orm_mode = True

class DocumentCreate(BaseModel):
    title: str

class DocumentResponse(BaseModel):
    id: int
    title: str
    file_path: str
    is_processed: bool

    class Config:
        orm_mode = True