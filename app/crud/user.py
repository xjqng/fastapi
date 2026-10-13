# app/crud/user.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db_models import User


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    """按 ID 查用户"""
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    """按用户名查用户"""
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """按邮箱查用户"""
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def create_user(
    db: AsyncSession,
    username: str,
    email: str,
    hashed_password: str,
) -> User:
    """创建用户，返回带 id 的 ORM 对象"""
    user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)   # 拿回自增 id 和默认值
    return user