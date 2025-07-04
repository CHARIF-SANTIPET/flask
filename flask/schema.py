from pydantic import BaseModel, Field
import datetime
import decimal


class ItemBase(BaseModel):
    created_at: datetime.datetime | None = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime | None = Field(default_factory=datetime.datetime.now)
    weight: float = 0.0
    service_price: decimal.Decimal = 0.0


# Pydantic -> ORM
class ItemCreate(ItemBase):
    pass


# ORM -> Pydantic
class ItemResponse(ItemBase):
    id: int

    class Config:
        from_attribute = True
