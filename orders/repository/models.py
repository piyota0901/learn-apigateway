import uuid
from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey
# https://docs.sqlalchemy.org/en/20/orm/quickstart.html#declare-models
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


def generate_uuid():
    return str(uuid.uuid4())

class OrderModel(Base):
    __tablename__ = "order"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=generate_uuid)
    items: Mapped[List["OrderItemModel"]] = relationship(back_populates="order")
    status: Mapped[str] = mapped_column(nullable=False, default="created")
    created: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    schedule_id: Mapped[str] = mapped_column()
    delivery_id: Mapped[str] = mapped_column()
    
    def dict(self):
        return {
            "id": self.id,
            "items": [item.dict() for item in self.items],
            "status": self.status,
            "created": self.created,
            "schedule_id": self.schedule_id,
            "delivery_id": self.delivery_id
        }


class OrderItemModel(Base):
    __tablename__ = "order_item"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=generate_uuid)
    order_id: Mapped[str] = mapped_column(ForeignKey("order.id"))
    product: Mapped[str] = mapped_column(nullable=False)
    size: Mapped[str] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    
    def dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "product": self.product,
            "size": self.size,
            "quantity": self.quantity
        }
