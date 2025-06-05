from fastapi import APIRouter
from services.gpt import ask_assistant

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "TurbotaBot is running."}


@router.post("/ask")
async def ask(user_id: int, message: str):
    """Return assistant reply for the given user message."""
    reply = await ask_assistant(user_id, message)
    return {"reply": reply}
