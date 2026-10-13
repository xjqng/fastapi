# app/services/favorite_service.py
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import favorite as crud_favorite
from app.crud import item as crud_item
from app.models.db_models import Favorite, User
from app.schemas.favorite import FavoriteCreate, FavoriteResponse, FavoriteListResponse


async def add_favorite(
    db: AsyncSession,
    data: FavoriteCreate,
    current_user: User,
) -> Favorite:
    """收藏：确认物品存在，且未重复收藏"""
    item = await crud_item.get_item_by_id(db, data.item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="物品不存在",
        )

    existing = await crud_favorite.get_favorite(db, current_user.id, data.item_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="已经收藏过该物品",
        )

    return await crud_favorite.create_favorite(
        db, user_id=current_user.id, item_id=data.item_id
    )


async def list_favorites(
    db: AsyncSession,
    current_user: User,
    page: int = 1,
    size: int = 10,
) -> FavoriteListResponse:
    """查当前用户的收藏列表"""
    if page < 1:
        page = 1
    if size < 1 or size > 100:
        size = 10

    favorites, total = await crud_favorite.get_favorites_by_user(
        db, user_id=current_user.id, page=page, size=size
    )
    return FavoriteListResponse(
        total=total,
        page=page,
        size=size,
        items=[FavoriteResponse.model_validate(f) for f in favorites],
    )


async def remove_favorite(
    db: AsyncSession,
    item_id: int,
    current_user: User,
) -> None:
    """取消收藏：只能取消自己的收藏"""
    favorite = await crud_favorite.get_favorite(db, current_user.id, item_id)
    if favorite is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="未收藏该物品",
        )

    await crud_favorite.delete_favorite(db, favorite)