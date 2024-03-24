from typing import List

from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship


class Base(AsyncAttrs, DeclarativeBase):
    pass


class CustomerORM(Base):
    __tablename__ = "Customers"
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String(50), nullable=False)
    orders: Mapped[List["OrderORM"]] = relationship(
        "OrderORM", back_populates="customer", cascade="all, delete-orphan"
    )


class OrderORM(Base):
    __tablename__ = "Orders"
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    quantity: Mapped[int] = Column(Integer, nullable=False)
    price: Mapped[float] = Column(Float, nullable=False)
    customer_id: Mapped[int] = Column(Integer, ForeignKey(CustomerORM.id))
    customer: Mapped[CustomerORM] = relationship("CustomerORM", back_populates="orders")

