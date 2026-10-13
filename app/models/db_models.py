# app/models/db_models.py
from datetime import datetime, UTC
from sqlalchemy import (
    ForeignKey, Text, DateTime, String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, comment="主键ID")
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True, comment="用户名")
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True, comment="邮箱")
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False, comment="加密密码")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC), comment="创建时间")

    # 关系
    items: Mapped[list["Item"]] = relationship(back_populates="owner")
    comments: Mapped[list["Comment"]] = relationship(back_populates="owner")
    favorites: Mapped[list["Favorite"]] = relationship(back_populates="user")


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, comment="主键ID")
    title: Mapped[str] = mapped_column(String(100), nullable=False, index=True, comment="物品标题")
    description: Mapped[str | None] = mapped_column(Text, nullable=True, comment="物品描述")
    price: Mapped[int] = mapped_column(comment="价格")
    view_count: Mapped[int] = mapped_column(default=0, comment="浏览次数")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC), comment="创建时间")

    # 关系
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, comment="发布用户ID")
    owner: Mapped["User"] = relationship(back_populates="items", lazy="selectin")

    comments: Mapped[list["Comment"]] = relationship(back_populates="item")
    favorites: Mapped[list["Favorite"]] = relationship(back_populates="item")


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, comment="主键ID")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="评论内容")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC), comment="创建时间")

    # 关系
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, comment="评论用户ID")
    owner: Mapped["User"] = relationship(back_populates="comments", lazy="selectin")

    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"), nullable=False, comment="所属物品ID")
    item: Mapped["Item"] = relationship(back_populates="comments")


class Favorite(Base):
    __tablename__ = "favorites"
    __table_args__ = (
        UniqueConstraint("user_id", "item_id", name="uq_user_item_favorite"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True, comment="主键ID")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC), comment="收藏时间")

    # 关系
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, comment="用户ID")
    user: Mapped["User"] = relationship(back_populates="favorites")

    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"), nullable=False, comment="物品ID")
    item: Mapped["Item"] = relationship(back_populates="favorites")