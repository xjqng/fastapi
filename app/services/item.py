# app/services/item_service.py
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import item as crud_item
from app.models.db_models import Item, User
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse, ItemListResponse


async def create_item(db: AsyncSession, data: ItemCreate, current_user: User) -> Item:
    """发布物品，owner_id 从当前登录用户拿"""
    return await crud_item.create_item(
        db,
        title=data.title,
        description=data.description,
        price=data.price,
        owner_id=current_user.id,
    )


async def list_items(db: AsyncSession, page: int = 1, size: int = 10) -> ItemListResponse:
    """分页查物品列表"""
    if page < 1:
        page = 1
    if size < 1 or size > 100:
        size = 10

    items, total = await crud_item.get_items(db, page=page, size=size)
    return ItemListResponse(
        total=total,
        page=page,
        size=size,
        items=[ItemResponse.model_validate(i) for i in items],
    )


async def get_item_detail(db: AsyncSession, item_id: int) -> Item:
    """查物品详情，不存在抛 404"""
    item = await crud_item.get_item_by_id(db, item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="物品不存在",
        )
    return item


async def update_item(
    db: AsyncSession,
    item_id: int,
    data: ItemUpdate,
    current_user: User,
) -> Item:
    """修改物品，只有发布者本人能改"""
    item = await get_item_detail(db, item_id)

    # 归属校验
    if item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权修改他人的物品",
        )

    # 只更新传了的字段
    fields = data.model_dump(exclude_unset=True)
    if not fields:
        return item

    return await crud_item.update_item(db, item, **fields)


async def delete_item(db: AsyncSession, item_id: int, current_user: User) -> None:
    """删除物品，只有发布者本人能删"""
    item = await get_item_detail(db, item_id)

    if item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权删除他人的物品",
        )

    await crud_item.delete_item(db, item)


async def view_item(db: AsyncSession, item_id: int) -> Item:
    """查看物品详情，浏览数 +1"""
    item = await get_item_detail(db, item_id)
    await crud_item.increment_view_count(db, item)
    return item