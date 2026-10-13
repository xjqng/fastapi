# app/schemas/item.py
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.user import UserSimple

# ---------- 请求模型 ----------
class ItemCreate(BaseModel):
    """发布物品请求体"""
    title: str = Field(..., min_length=1, max_length=100, description="物品标题")
    description: str | None = Field(None, max_length=2000, description="物品描述")
    price: int = Field(..., ge=0, description="价格，单位分")

class ItemUpdate(BaseModel):
    """修改物品请求体，全部可选，只传要改的字段"""
    title: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, max_length=2000)
    price: int | None = Field(None, ge=0)

# ---------- 响应模型 ----------
class ItemResponse(BaseModel):
    """物品公开信息"""
    id: int
    title: str
    description: str | None
    price: int
    view_count: int
    owner_id: int
    owner: UserSimple
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ItemListResponse(BaseModel):
    """分页列表响应"""
    total: int
    page: int
    size: int
    items: list[ItemResponse]
