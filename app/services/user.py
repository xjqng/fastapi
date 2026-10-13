# app/services/user_service.py
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import user as crud_user
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token,
)
from app.schemas.user import UserCreate, UserResponse, Token


async def register_user(db: AsyncSession, data: UserCreate) -> Token:
    """注册：查重 → 哈希密码 → 建用户 → 签发 token"""
    # 1. 用户名查重
    if await crud_user.get_user_by_username(db, data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在",
        )

    # 2. 邮箱查重
    if await crud_user.get_user_by_email(db, data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被注册",
        )

    # 3. 哈希密码 + 创建用户
    hashed = hash_password(data.password)
    user = await crud_user.create_user(
        db,
        username=data.username,
        email=data.email,
        hashed_password=hashed,
    )

    # 4. 签发 token
    return Token(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )


async def login_user(db: AsyncSession, username: str, password: str) -> Token:
    """登录：查用户 → 验密码 → 签发 token"""
    user = await crud_user.get_user_by_username(db, username)

    # 用户不存在 / 密码错误，统一返回同一个提示，不暴露哪个错了
    if user is None or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return Token(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )


async def refresh_access_token(db: AsyncSession, refresh_token: str) -> Token:
    """用 refresh token 换新 token"""
    payload = verify_token(refresh_token, expected_type="refresh")
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="refresh token 无效或已过期",
        )

    user_id_str = payload.get("sub")
    if user_id_str is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="refresh token 无效",
        )

    # 确认用户还存在（可能被删了）
    user = await crud_user.get_user_by_id(db, int(user_id_str))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
        )

    return Token(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )