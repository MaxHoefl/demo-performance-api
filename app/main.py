import uvicorn
from fastapi import FastAPI, Depends
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.data_acess.db import setup_database, create_session
from app.data_acess.repositories import acquire_order_repository, OrderRepository

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    logger.info("Running startup actions")
    await setup_database(initialize_sample_data=True)
    logger.info("Startup actions complete")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/orders/{customer_id}")
async def get_orders_by_customer(customer_id: int,
                                 session: AsyncSession = Depends(create_session),
                                 repo: OrderRepository = Depends(acquire_order_repository)):
    logger.info("Endpoint /orders/customer_id called")
    res = await repo.get_orders_for_customer(customer_id, session)
    return res

# @app.get("/_cache")
# def get_cache_data(repo: OrderRepository = Depends(acquire_order_repository)):
#     cache_data = repo.get_orders_for_customer.cache._Cache__data
#     cache_info = repo.get_orders_for_customer.cache_info()
#     return {
#         "method": "get_orders_for_customer",
#         "stats": {
#             "hits": cache_info.hits,
#             "misses": cache_info.misses,
#             "maxsize": cache_info.maxsize
#         },
#         "data": {
#             cache_data.key[0]: cache_data.value
#         }
#     }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080)
