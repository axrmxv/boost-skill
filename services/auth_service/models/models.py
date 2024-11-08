"""
Определение моделей базы данных с использованием ORM SQLAlchemy.
Здесь описываются структуры данных, которые будут храниться в базе.
"""
import datetime

from sqlalchemy import String, BigInteger, Column
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func


class Base(AsyncAttrs, DeclarativeBase):
    pass


class BaseModelMixin:
    """
    When used as a base class, it allows you to define
    a set of common properties
    that can be applied to subsequent classes.
    """
    @declared_attr.directive
    def tablename(cls) -> str:
        return cls.name.lower()  # type: ignore

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    created_at: Mapped[datetime.datetime] = mapped_column(
        default=func.now(), server_default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        default=func.now(), onupdate=func.now(), server_default=func.now()
    )


class Client(BaseModelMixin, Base):
    client_id: Mapped[str] = mapped_column(String(50), unique=True)
    client_secret: Mapped[str] = mapped_column(String(50))
    client_name: Mapped[str] = mapped_column(String(50))
