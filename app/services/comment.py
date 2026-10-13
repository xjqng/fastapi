# app/services/comment_service.py
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import comment as crud_comment
from app.crud import item as crud_item
from app.models.db_models import Comment, User
from app.schemas.comment import CommentCreate, CommentResponse, CommentListResponse


async def create_comment(
    db: AsyncSession,
    item_id: int,
    data: CommentCreate,
    current_user: User,
) -> Comment:
    """发表评论：先确认物品存在，再创建"""
    item = await crud_item.get_item_by_id(db, item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="物品不存在",
        )

    return await crud_comment.create_comment(
        db,
        content=data.content,
        item_id=item_id,
        owner_id=current_user.id,
    )


async def list_comments(
    db: AsyncSession,
    item_id: int,
    page: int = 1,
    size: int = 10,
) -> CommentListResponse:
    """查某个物品的评论列表"""
    if page < 1:
        page = 1
    if size < 1 or size > 100:
        size = 10

    comments, total = await crud_comment.get_comments_by_item(
        db, item_id=item_id, page=page, size=size
    )
    return CommentListResponse(
        total=total,
        page=page,
        size=size,
        items=[CommentResponse.model_validate(c) for c in comments],
    )


async def delete_comment(
    db: AsyncSession,
    comment_id: int,
    current_user: User,
) -> None:
    """删除评论：只有评论作者本人能删"""
    comment = await crud_comment.get_comment_by_id(db, comment_id)
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="评论不存在",
        )

    if comment.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权删除他人的评论",
        )

    await crud_comment.delete_comment(db, comment)