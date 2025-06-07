from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio
from turbota_app.bot import start_bot
from turbota_app.routers import base
from turbota_app.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    asyncio.create_task(start_bot())
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(base.router)

