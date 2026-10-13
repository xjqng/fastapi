# app/crud/comment.py
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db_models import Comment


async def get_comment_by_id(db: AsyncSession, comment_id: int) -> Comment | None:
    """按 ID 查评论"""
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    return result.scalar_one_or_none()


async def get_comments_by_item(
    db: AsyncSession,
    item_id: int,
    page: int = 1,
    size: int = 10,
) -> tuple[list[Comment], int]:
    """按物品分页查评论"""
    count_result = await db.execute(
        select(func.count()).select_from(Comment).where(Comment.item_id == item_id)
    )
    total = count_result.scalar_one()

    offset = (page - 1) * size
    result = await db.execute(
        select(Comment)
        .where(Comment.item_id == item_id)
        .order_by(Comment.created_at.desc())
        .offset(offset)
        .limit(size)
    )
    comments = list(result.scalars().all())
    return comments, total


async def create_comment(
    db: AsyncSession,
    content: str,
    item_id: int,
    owner_id: int,
) -> Comment:
    """创建评论"""
    comment = Comment(content=content, item_id=item_id, owner_id=owner_id)
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment


async def delete_comment(db: AsyncSession, comment: Comment) -> None:
    """删除评论"""
    await db.delete(comment)
    await db.commit()