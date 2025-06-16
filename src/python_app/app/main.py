from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Dict
import datetime
import uuid
import jwt
import subprocess
import os

app = FastAPI(
        title="QynAuth API - MVP",
        description=(
            "API for Quantum-resistant Authentication (MVP) in the Minkalla QynAuth module. "
            "Currently uses classical authentication with quantum-safe placeholders."
        ),
        version="1.0.0",
    )

user_db: Dict[str, Dict[str, str]] = {}

SECRET_KEY = "your-super-secret-key"
ALGORITHM = "HS256"


class RegisterRequest(BaseModel):
        username: str
        password: str


class RegisterResponse(BaseModel):
        message: str
        user_id: str
        username: str


class LoginRequest(BaseModel):
        username: str
        password: str


class LoginResponse(BaseModel):
        access_token: str
        token_type: str = "bearer"
        user_id: str


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
        """
        Registers a new user with a unique username and password.
        For MVP, uses in-memory storage. Password hashing is a placeholder.
        """
        if request.username in user_db:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already registered",
            )

        hashed_password = f"MOCKED_HASH_{request.password}"

        user_id = str(uuid.uuid4())

        user_db[request.username] = {
            "password_hash": hashed_password,
            "user_id": user_id,
            "created_at": datetime.datetime.utcnow().isoformat(),
        }

        print(f"[VERIFIABLE LOG]: User {request.username} registered with ID {user_id}")

        try:
            simulated_rust_output = subprocess.run(
                ["echo", "Simulated Rust PQC call: Operation success!"],
                capture_output=True,
                text=True,
                check=True,
            )
            print(
                f"[VERIFIABLE LOG]: Rust subprocess simulation: "
                f"{simulated_rust_output.stdout.strip()}"
            )
        except subprocess.CalledProcessError as e:
            print(f"[ERROR]: Rust subprocess simulation failed: {e}")

        return {
            "message": "User registered successfully",
            "user_id": user_id,
            "username": request.username,
        }


@app.post(
        "/auth/login",
        response_model=LoginResponse,
        summary="Authenticate user and return JWT",
    )
async def login_for_access_token(request: LoginRequest):
        """
        Authenticates a user with username and password.
        Returns a JWT access token upon successful authentication.
        """
        user = user_db.get(request.username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=("Incorrect username or password"),  # Broken for E501
                headers={"WWW-Authenticate": "Bearer"},
            )

        if user["password_hash"] != f"MOCKED_HASH_{request.password}":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=("Incorrect username or password"),  # Broken for E501
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = datetime.timedelta(minutes=30)
        to_encode = {"sub": user["user_id"]}
        expire = datetime.datetime.utcnow() + access_token_expires
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        print(f"[VERIFIABLE LOG]: User {request.username} logged in, issued JWT")

        return {
            "access_token": encoded_jwt,
            "token_type": "bearer",
            "user_id": user["user_id"],
        }