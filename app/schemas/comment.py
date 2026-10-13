# app/schemas/comment.py
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.user import UserSimple

# ---------- 请求模型 ----------
class CommentCreate(BaseModel):
    """发表评论请求体"""
    content: str = Field(..., min_length=1, max_length=1000, description="评论内容")

# ---------- 响应模型 ----------
class CommentResponse(BaseModel):
    """评论公开信息"""
    id: int
    content: str
    item_id: int
    owner_id: int
    owner: UserSimple
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class CommentListResponse(BaseModel):
    """评论分页列表"""
    total: int
    page: int
    size: int
    items: list[CommentResponse]
