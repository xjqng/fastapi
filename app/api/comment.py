# app/api/comment.py
from fastapi import APIRouter, Query, status

from app.api.deps import DbSession, CurrentUser
from app.schemas.comment import CommentCreate, CommentResponse, CommentListResponse
from app.services import comment as comment_service

router = APIRouter(tags=["评论"])


@router.post(
    "/items/{item_id}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(
    item_id: int,
    data: CommentCreate,
    db: DbSession,
    current_user: CurrentUser,
):
    """对物品发表评论（需登录）"""
    return await comment_service.create_comment(db, item_id, data, current_user)


@router.get("/items/{item_id}/comments", response_model=CommentListResponse)
async def list_comments(
    item_id: int,
    db: DbSession,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
):
    """查看某物品的评论列表（无需登录）"""
    return await comment_service.list_comments(db, item_id, page=page, size=size)


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    db: DbSession,
    current_user: CurrentUser,
):
    """删除评论，仅评论作者本人（需登录）"""
    await comment_service.delete_comment(db, comment_id, current_user)