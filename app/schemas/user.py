# app/schemas/user.py
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

# ---------------- 请求模型（前端传给后端） ----------------
class UserCreate(BaseModel):
    """用户注册请求体"""
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    """用户登录请求体"""
    username: str
    password: str

# ---------------- 响应模型（后端返回给前端） ----------------
class UserSimple(BaseModel):
    """简单用户信息，用于物品、评论里面嵌套展示作者，不暴露邮箱"""
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str

class UserResponse(BaseModel):
    """完整用户信息响应，个人主页使用"""
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: str
    created_at: datetime

# -------------------- jwt ------------------------------------
class Token(BaseModel):
    """登录/注册成功后返回的 token"""
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    """解析 JWT 后的载荷（内部用）"""
    sub: str          # user_id，JWT 规范要求字符串
    exp: int
    type: str         # "access" 或 "refresh"
