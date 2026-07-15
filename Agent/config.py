from pathlib import Path
from dotenv import load_dotenv
import os

current = Path(__file__)

BASE_DIR = current.resolve().parent
DATABASE_DIR = BASE_DIR.parent
print(DATABASE_DIR)


env = BASE_DIR / "keys.env"

load_dotenv(env)
api_key = os.getenv("GOOGLE_API_KEY")

MODEL = "gemini-2.5-flash"