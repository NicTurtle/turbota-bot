from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio
from bot import start_bot
from routers import base

@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(start_bot())
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(base.router)
