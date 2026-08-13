"""
Auth API Router
"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from app.dependencies import auth_service

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


class RegisterRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/register")
def register(payload: RegisterRequest):
    try:
        return auth_service.register(payload.email, payload.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(payload: LoginRequest):
    try:
        return auth_service.authenticate(payload.email, payload.password)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Dependency other routes can use to require a logged-in user.
    Usage: def my_route(user: dict = Depends(get_current_user)):
    """
    try:
        return auth_service.verify_token(token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get("/me")
def me(user: dict = Depends(get_current_user)):
    return user