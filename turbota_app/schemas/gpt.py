from pydantic import BaseModel

class GPTRequest(BaseModel):
    user_id: int
    message: str

class GPTResponse(BaseModel):
    reply: str
