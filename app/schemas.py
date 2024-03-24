from pydantic import BaseModel, ConfigDict, Field


class DataModel(BaseModel):
    class Config:
        from_attributes = True
        orm_mode = True


class Customer(DataModel):
    id: int
    name: str


class Order(DataModel):
    id: int
    quantity: int
    price: float
    customer_id: int
    customer: Customer = Field(default=None)
