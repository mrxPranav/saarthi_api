import os
import secrets

from dotenv import load_dotenv
from fastapi import Header, HTTPException, status

load_dotenv()

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    # Fail closed: never run an unauthenticated API.
    raise RuntimeError("API_KEY is not set. Add it to app/.env or the environment.")


async def verify_api_key(x_api_key: str | None = Header(default=None)) -> None:
    if x_api_key is None or not secrets.compare_digest(x_api_key, API_KEY):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
