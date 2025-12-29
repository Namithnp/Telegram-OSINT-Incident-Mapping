from pathlib import Path
from dotenv import load_dotenv
from pyrogram import Client
import os

load_dotenv()

TG_API_ID = int(os.getenv("TG_API_ID"))
TG_API_HASH = os.getenv("TG_API_HASH")

BASE_DIR = Path(__file__).resolve().parent
SESSION_PATH = BASE_DIR / "my_account"

_client = None


def get_telegram_client() -> Client:
    global _client

    if _client is None:
        _client = Client(
            name=str(SESSION_PATH),  # ABSOLUTE PATH
            api_id=TG_API_ID,
            api_hash=TG_API_HASH,
        )

    return _client
