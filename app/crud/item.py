# app/crud/item.py
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db_models import Item


async def get_item_by_id(db: AsyncSession, item_id: int) -> Item | None:
    """按 ID 查物品"""
    result = await db.execute(select(Item).where(Item.id == item_id))
    return result.scalar_one_or_none()


async def get_items(
    db: AsyncSession,
    page: int = 1,
    size: int = 10,
) -> tuple[list[Item], int]:
    """分页查物品列表，返回 (当前页数据, 总数)"""
    # 总数
    count_result = await db.execute(select(func.count()).select_from(Item))
    total = count_result.scalar_one()

    # 当前页
    offset = (page - 1) * size
    result = await db.execute(
        select(Item).order_by(Item.created_at.desc()).offset(offset).limit(size)
    )
    items = list(result.scalars().all())
    return items, total


async def get_items_by_owner(
    db: AsyncSession,
    owner_id: int,
    page: int = 1,
    size: int = 10,
) -> tuple[list[Item], int]:
    """按发布者分页查物品"""
    count_result = await db.execute(
        select(func.count()).select_from(Item).where(Item.owner_id == owner_id)
    )
    total = count_result.scalar_one()

    offset = (page - 1) * size
    result = await db.execute(
        select(Item)
        .where(Item.owner_id == owner_id)
        .order_by(Item.created_at.desc())
        .offset(offset)
        .limit(size)
    )
    items = list(result.scalars().all())
    return items, total


async def create_item(
    db: AsyncSession,
    title: str,
    description: str | None,
    price: int,
    owner_id: int,
) -> Item:
    """创建物品"""
    item = Item(
        title=title,
        description=description,
        price=price,
        owner_id=owner_id,
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


async def update_item(db: AsyncSession, item: Item, **fields) -> Item:
    """更新物品，只改传入的字段"""
    for key, value in fields.items():
        setattr(item, key, value)
    await db.commit()
    await db.refresh(item)
    return item


async def delete_item(db: AsyncSession, item: Item) -> None:
    """删除物品"""
    await db.delete(item)
    await db.commit()


async def increment_view_count(db: AsyncSession, item: Item) -> None:
    """浏览次数 +1（数据库层，非 Redis）"""
    item.view_count += 1
    await db.commit()