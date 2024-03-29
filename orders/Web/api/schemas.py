from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Extra, conint, conlist, validator

class Size(Enum):
    small = "small"
    medium = "medium"
    large = "large"

class StatusEnum(Enum):
    created = "created"
    paid = "paid"
    progress = "progress"
    cancelled = "cancelled"
    dispatched = "dispatched"
    delivered = "delivered"

class OrderItemSchema(BaseModel):
    product: str
    size: Size
    quantity: Optional[conint(ge=1, strict=True)] = 1
    
    @validator('quantity')
    def quantity_non_nullable(cls, value):
        assert value is not None, 'quantity may no be None'
        return value

    class Config:
        # https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.extra
        extra = "forbid"

class CreateOrderSchema(BaseModel):
    order: conlist(OrderItemSchema, min_length=1)
    
    class Config:
        # https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.extra
        extra = "forbid"

class GetOrderSchema(CreateOrderSchema):
    id: UUID
    created: datetime
    status: StatusEnum

class GetOrdersSchema(BaseModel):
    orders: List[GetOrderSchema]
    
    class Config:
        extra = "forbid"
