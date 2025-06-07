from pydantic import BaseModel
from datetime import datetime

class Message(BaseModel):
    user_id: int
    role: str  # 'user' or 'assistant'
    text: str
    timestamp: datetime
