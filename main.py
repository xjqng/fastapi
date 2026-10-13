# main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, item, comment, favorite
from app.db.session import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用启动时建表（开发环境用，生产用 Alembic）"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="二手交易 API",
    description="FastAPI + MySQL + Redis 二手物品交易后端",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # 生产要改成具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router)
app.include_router(item.router)
app.include_router(comment.router)
app.include_router(favorite.router)


@app.get("/", tags=["根"])
async def root():
    return {"message": "二手交易 API 运行中", "docs": "/docs"}