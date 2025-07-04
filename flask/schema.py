from pydantic import BaseModel, Field
import datetime
import decimal


class ItemBase(BaseModel):
    weight: float = 0.0
    service_price: decimal.Decimal = 0.0
    receiver_id: int


# Pydantic -> ORM
class ItemCreate(ItemBase):
    pass


# ORM -> Pydantic
class ItemResponse(ItemBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attribute = True


class ReceiverBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    address: str = Field(..., min_length=1, max_length=200)
    phone_number: str = Field(..., min_length=10, max_length=15)
    # created_at: datetime.datetime | None = Field(default_factory=datetime.datetime.now)
    # updated_at: datetime.datetime | None = Field(default_factory=datetime.datetime.now)


class ReceiverCreate(ReceiverBase):
    pass


class ReceiverResponse(ReceiverBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attribute = True


class ItemWithReceiverResponse(ItemResponse):
    receiver: ReceiverResponse

    class Config:
        from_attribute = True


class ReceiverWithItemsResponse(ReceiverResponse):
    items: list[ItemResponse] = []

    class Config:
        from_attribute = True
