# app/crud/favorite.py
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db_models import Favorite


async def get_favorite(db: AsyncSession, user_id: int, item_id: int) -> Favorite | None:
    """查某个用户是否收藏了某个物品"""
    result = await db.execute(
        select(Favorite).where(
            Favorite.user_id == user_id,
            Favorite.item_id == item_id,
        )
    )
    return result.scalar_one_or_none()


async def get_favorites_by_user(
    db: AsyncSession,
    user_id: int,
    page: int = 1,
    size: int = 10,
) -> tuple[list[Favorite], int]:
    """按用户分页查收藏"""
    count_result = await db.execute(
        select(func.count()).select_from(Favorite).where(Favorite.user_id == user_id)
    )
    total = count_result.scalar_one()

    offset = (page - 1) * size
    result = await db.execute(
        select(Favorite)
        .where(Favorite.user_id == user_id)
        .order_by(Favorite.created_at.desc())
        .offset(offset)
        .limit(size)
    )
    favorites = list(result.scalars().all())
    return favorites, total


async def create_favorite(db: AsyncSession, user_id: int, item_id: int) -> Favorite:
    """创建收藏"""
    favorite = Favorite(user_id=user_id, item_id=item_id)
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)
    return favorite


async def delete_favorite(db: AsyncSession, favorite: Favorite) -> None:
    """取消收藏"""
    await db.delete(favorite)
    await db.commit()