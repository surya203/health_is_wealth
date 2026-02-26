import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API = (os.getenv("OPENAI_API") or "").strip()
if not OPENAI_API or OPENAI_API == "None":
    raise ValueError(
        "OPENAI_API_KEY is missing or invalid. Set it in .env or environment."
    )
MODEL_NAME = "gpt-4o-mini"