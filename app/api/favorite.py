# app/api/favorite.py
from fastapi import APIRouter, Query, status

from app.api.deps import DbSession, CurrentUser
from app.schemas.favorite import FavoriteCreate, FavoriteResponse, FavoriteListResponse
from app.services import favorite as favorite_service

router = APIRouter(prefix="/favorites", tags=["收藏"])


@router.post("", response_model=FavoriteResponse, status_code=status.HTTP_201_CREATED)
async def add_favorite(data: FavoriteCreate, db: DbSession, current_user: CurrentUser):
    """收藏物品（需登录）"""
    return await favorite_service.add_favorite(db, data, current_user)


@router.get("", response_model=FavoriteListResponse)
async def list_favorites(
    db: DbSession,
    current_user: CurrentUser,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
):
    """查看我的收藏列表（需登录）"""
    return await favorite_service.list_favorites(db, current_user, page=page, size=size)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_favorite(item_id: int, db: DbSession, current_user: CurrentUser):
    """取消收藏（需登录）"""
    await favorite_service.remove_favorite(db, item_id, current_user)