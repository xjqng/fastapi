# app/api/item.py
from fastapi import APIRouter, Query, status

from app.api.deps import DbSession, CurrentUser
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse, ItemListResponse
from app.services import item as item_service

router = APIRouter(prefix="/items", tags=["物品"])


@router.post("", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(data: ItemCreate, db: DbSession, current_user: CurrentUser):
    """发布物品（需登录）"""
    return await item_service.create_item(db, data, current_user)


@router.get("", response_model=ItemListResponse)
async def list_items(
    db: DbSession,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
):
    """物品列表，分页（无需登录）"""
    return await item_service.list_items(db, page=page, size=size)


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int, db: DbSession):
    """物品详情，浏览数 +1（无需登录）"""
    return await item_service.view_item(db, item_id)


@router.patch("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int,
    data: ItemUpdate,
    db: DbSession,
    current_user: CurrentUser,
):
    """修改物品，仅发布者本人（需登录）"""
    return await item_service.update_item(db, item_id, data, current_user)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, db: DbSession, current_user: CurrentUser):
    """删除物品，仅发布者本人（需登录）"""
    await item_service.delete_item(db, item_id, current_user)