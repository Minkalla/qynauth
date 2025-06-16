from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Dict, List
import datetime
import uuid

app = FastAPI(
    title="QynAuth API - MVP",
    description="API for Quantum-resistant Authentication (MVP) in the Minkalla QynAuth module. Currently uses classical authentication with quantum-safe placeholders.",
    version="1.0.0",
)

user_db: Dict[str, Dict[str, str]] = {}

class RegisterRequest(BaseModel):
    username: str
    password: str

class RegisterResponse(BaseModel):
    message: str
    user_id: str
    username: str

@app.get("/health", summary="Health check endpoint")
async def health_check():
    return {"status": "ok", "service": "QynAuth MVP"}


@app.post(
    "/auth/register",
    response_model=RegisterResponse,
    summary="Register a new user",
    status_code=status.HTTP_201_CREATED,
)
async def register_user(request: RegisterRequest):
    if request.username in user_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already registered",
        )

    # For MVP, we'll store a mock hash or the plain password (NOT for production!)
    hashed_password = f"MOCKED_HASH_{request.password}"

    user_id = str(uuid.uuid4())

    user_db[request.username] = {
        "password_hash": hashed_password,
        "user_id": user_id,
        "created_at": datetime.datetime.utcnow().isoformat(),
    }

    print(f"[VERIFIABLE LOG]: User {request.username} registered with ID {user_id}")

    return {
        "message": "User registered successfully",
        "user_id": user_id,
        "username": request.username,
    }
