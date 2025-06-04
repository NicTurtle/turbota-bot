from pydantic import BaseModel

class GPTRequest(BaseModel):
    prompt: str

class GPTResponse(BaseModel):
    response: str
