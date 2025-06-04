from fastapi import APIRouter
from schemas.gpt import GPTResponse, GPTRequest
from schemas.history import MessageIn, MessageOut
from services.gpt import ask_gpt
from services.history import save_message, get_last_messages
from fastapi import Query
from typing import List

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "TurbotaBot is running."}

@router.post("/ask")
async def ask_gpt_api(message: MessageIn):
    history = await get_last_messages(user_id=message.user_id)  # убрали limit
    answer = await ask_gpt(message.text, history, message.user_id)

    await save_message(MessageIn(
        user_id=message.user_id,
        text=message.text,
        answer=answer
    ))

    return {"answer": answer}

@router.post("/save-message")
async def save_msg(msg: MessageIn):
    await save_message(msg)
    return {"status": "ok"}

@router.get("/history", response_model=List[MessageOut])
async def history(user_id: int = Query(...), limit: int = Query(5)):
    return await get_last_messages(user_id, limit)
