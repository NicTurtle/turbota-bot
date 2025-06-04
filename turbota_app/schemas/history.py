from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MessageIn(BaseModel):
    user_id: int
    text: str
    answer: str

class MessageOut(MessageIn):
    id: int
    created_at: datetime
