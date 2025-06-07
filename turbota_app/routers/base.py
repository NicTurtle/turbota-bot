from fastapi import APIRouter
from turbota_app.schemas.gpt import GPTRequest, GPTResponse
from turbota_app.services.gpt import ask_assistant

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "TurbotaBot is running."}

@router.post("/ask", response_model=GPTResponse)
async def ask(data: GPTRequest):
    reply = await ask_assistant(data.user_id, data.message)
    return GPTResponse(reply = reply)