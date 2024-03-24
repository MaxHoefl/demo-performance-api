import random

from loguru import logger
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.config import acquire_app_config
from app.data_acess.models import Base, CustomerORM, OrderORM

config = acquire_app_config()
engine = create_async_engine(
    url=config.db_url, echo=False
)
session_maker = async_sessionmaker(engine)


async def create_session() -> AsyncSession:
    logger.info("Creating async session")
    session = session_maker()
    try:
        async with session:
            logger.info("Yielding session")
            yield session
            logger.info("Yield session done")
    finally:
        logger.info("Closing session")
        await session.close()


async def insert_sample_data(session_maker: async_sessionmaker[AsyncSession]):
    logger.info("Inserting sample data")
    sample_customers = [
        CustomerORM(name="Mary"),
        CustomerORM(name="Greg"),
        CustomerORM(name="John")
    ]
    num_orders = 10
    quantities = [random.randint(1, 3) for _ in range(num_orders)]
    prices = [int(100 * random.uniform(5, 10)) / 100 for _ in range(num_orders)]
    sample_orders = [
        OrderORM(price=p, quantity=q, customer_id=random.randint(1, len(sample_customers)))
        for q, p in zip(quantities, prices)
    ]
    async with session_maker() as session:
        async with session.begin():
            session.add_all(sample_customers)
            session.add_all(sample_orders)
            await session.commit()


async def setup_database(initialize_sample_data: bool = False):
    logger.info("Setting up database")
    async with engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            await conn.commit()
        except Exception as e:
            logger.error(f"Error during database setup: {e}")
            raise e
        finally:
            await conn.close()
    if initialize_sample_data:
        await insert_sample_data(session_maker)
