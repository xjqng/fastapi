# app/api/auth.py
from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import DbSession
from app.schemas.user import UserCreate, Token, UserResponse
from app.services import user as user_service

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, db: DbSession):
    """注册，成功后直接返回 token"""
    return await user_service.register_user(db, data)


@router.post("/login", response_model=Token)
async def login(
    db: DbSession,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    """登录，用表单格式（username / password）"""
    return await user_service.login_user(db, form_data.username, form_data.password)


@router.post("/refresh", response_model=Token)
async def refresh(db: DbSession, refresh_token: str):
    """用 refresh token 换新 token"""
    return await user_service.refresh_access_token(db, refresh_token)