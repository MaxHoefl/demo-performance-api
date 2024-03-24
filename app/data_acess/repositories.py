import asyncio
from abc import ABC, abstractmethod
from typing import Union, List
from loguru import logger
from cachetools import LRUCache
from cachetools.keys import hashkey
from asyncache import cached
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, selectinload

from app.data_acess.models import OrderORM
from app.schemas import Order


class OrderRepository(ABC):
    @abstractmethod
    def get_orders_for_customer(self, customer_id, db: Union[AsyncSession, Session]):
        raise NotImplementedError


class SqlOrderRepository(OrderRepository):
    @cached(
        cache=LRUCache(maxsize=128),
        key=lambda self, customer_id, session: hashkey(customer_id)
    )
    async def get_orders_for_customer(self, customer_id, session: AsyncSession) -> List[Order]:
        stmt = select(OrderORM).where(OrderORM.customer_id == customer_id).options(selectinload(OrderORM.customer))
        logger.info(f"Getting orders for customer {customer_id} from database")
        result = await session.execute(stmt)
        return [Order.from_orm(order) for order in result.scalars()]


def acquire_order_repository():
    return SqlOrderRepository()