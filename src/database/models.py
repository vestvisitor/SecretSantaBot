from sqlalchemy import ForeignKey, String, MetaData, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import Optional


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    vk_id: Mapped[int]
    number: Mapped[int] = mapped_column(Integer)
    wishlist: Mapped[Optional[str]] = mapped_column(String)
    state: Mapped[int]
    active: Mapped[int]


class Decision(Base):
    __tablename__ = "decision"

    id: Mapped[int] = mapped_column(primary_key=True)
    giver: Mapped[int] = mapped_column(ForeignKey("user.name"))
    receiver: Mapped[int] = mapped_column(ForeignKey("user.name"))


class Wish(Base):
    __tablename__ = "wish"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    link: Mapped[str]
    code: Mapped[int]
    priority: Mapped[int]
    owner: Mapped[int] = mapped_column(ForeignKey("user.vk_id"))
