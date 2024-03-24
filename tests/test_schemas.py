from app.data_acess.models import CustomerORM, OrderORM
from app.schemas import Order


def test_order_schema_from_orm_model():
    order_orm = OrderORM(
        id=1,
        quantity=1,
        price=100,
        customer_id=1,
        customer=CustomerORM(
            id=1,
            name="Max"
        )
    )
    order = Order.from_orm(order_orm)
    assert order.id == 1
    assert order.quantity == 1
    assert order.price == 100
    assert order.customer_id == 1
    assert order.customer.id == 1
    assert order.customer.name == "Max"
