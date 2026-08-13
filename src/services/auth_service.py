"""
auth_service.py
Handles user registration, login, password hashing, and JWT tokens.
"""

from __future__ import annotations

import os
import sqlite3
from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_SECRET = os.getenv("JWT_SECRET", "insecure-dev-secret")
JWT_ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days


class AuthService:
    """
    Manages user accounts and authentication tokens.
    """

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._ensure_table()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _ensure_table(self):
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS Users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL UNIQUE,
                    hashed_password TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )

    # ---------------------------------------------------------
    # Register
    # ---------------------------------------------------------
    def register(self, email: str, password: str) -> dict:
        email = email.strip().lower()

        with self._connect() as conn:
            existing = conn.execute(
                "SELECT id FROM Users WHERE email = ?",
                (email,),
            ).fetchone()

            if existing:
                raise ValueError("An account with this email already exists.")

            hashed = pwd_context.hash(password)

            conn.execute(
                """
                INSERT INTO Users (email, hashed_password, created_at)
                VALUES (?, ?, ?)
                """,
                (email, hashed, datetime.now(timezone.utc).isoformat()),
            )

        return {"email": email, "status": "registered"}

    # ---------------------------------------------------------
    # Login
    # ---------------------------------------------------------
    def authenticate(self, email: str, password: str) -> dict:
        email = email.strip().lower()

        with self._connect() as conn:
            row = conn.execute(
                "SELECT id, email, hashed_password FROM Users WHERE email = ?",
                (email,),
            ).fetchone()

        if row is None:
            raise ValueError("Invalid email or password.")

        user_id, user_email, hashed_password = row

        if not pwd_context.verify(password, hashed_password):
            raise ValueError("Invalid email or password.")

        token = self._create_token(user_id, user_email)

        return {"access_token": token, "token_type": "bearer"}

    # ---------------------------------------------------------
    # Token Creation
    # ---------------------------------------------------------
    def _create_token(self, user_id: int, email: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=TOKEN_EXPIRE_MINUTES
        )
        payload = {
            "sub": str(user_id),
            "email": email,
            "exp": expire,
        }
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    # ---------------------------------------------------------
    # Token Verification
    # ---------------------------------------------------------
    def verify_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return {
                "user_id": int(payload["sub"]),
                "email": payload["email"],
            }
        except JWTError:
            raise ValueError("Invalid or expired token.")