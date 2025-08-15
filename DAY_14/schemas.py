from pydantic import BaseModel
from typing import List

class Message(BaseModel):
    role: str  # "user" or "ai"
    text: str

class ChatHistory(BaseModel):
    messages: List[Message]
