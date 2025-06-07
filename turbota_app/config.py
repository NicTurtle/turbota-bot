from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    TELEGRAM_TOKEN: str
    OPENAI_API_KEY: str
    DEBUG: bool = False
    DATABASE_PATH: str = "tmp/psychologist.db"

config = Settings(
    TELEGRAM_TOKEN=os.getenv("TELEGRAM_TOKEN"),
    OPENAI_API_KEY=os.getenv("OPENAI_API_KEY"),
    DEBUG=bool(int(os.getenv("DEBUG", "0"))),
    DATABASE_PATH=os.getenv("DATABASE_PATH", "tmp/psychologist.db")
)
