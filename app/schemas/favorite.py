# app/schemas/favorite.py
from datetime import datetime
from pydantic import BaseModel, ConfigDict

# ---------- 请求模型 ----------
class FavoriteCreate(BaseModel):
    """收藏请求体，只需要 item_id"""
    item_id: int

# ---------- 响应模型 ----------
class FavoriteResponse(BaseModel):
    """收藏记录"""
    id: int
    user_id: int
    item_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class FavoriteListResponse(BaseModel):
    """收藏分页列表"""
    total: int
    page: int
    size: int
    items: list[FavoriteResponse]
