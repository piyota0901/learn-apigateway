from orders.orders_service.orders import Order
from orders.repository.models import OrderModel, OrderItemModel

from sqlalchemy.orm import Session

from orders.Web.api.schemas import OrderItemSchema

class OrdersRepositry:
    
    def __init__(self, session: Session):
        self.session = session
        
    def add(self, items: list[OrderItemSchema]):
        record = OrderModel(items=[OrderItemModel(**item) for item in items])
        self.session.add(record)
        return Order(**record.dict(), order_=record)
    
    def _get(self, id_: str):
        return (
            self.session.query(OrderModel)
            .filter(OrderModel.id == str(id_))
            .first()
        )
    
    def get(self, id_: str):
        order = self._get(id_)
        if order is not None:
            return Order(**order.dict())
    
    
    def list(self, limit=None, **filters):
        query = self.session.query(OrderModel)
        if "cancelled" in filters:
            cancelled = filters.pop("cancelled")
            if cancelled:
                query = query.filter(OrderModel.status == "cancelled")
            else:
                query = query.filter(OrderModel.status != "cancelled")
        
        records = query.filter(**filters).limit(limit).all()
        return [Order(**record.dict()) for record in records]
    
    
    def update(self,id_: str, **payload):
        record = self._get(id_)
        if "items" in payload:
            for item in record.items:
                self.session.delete(item)
            record.item = [
                OrderItemModel(**item) for item in payload.pop("items")
            ]
        
        for key, value in payload.items():
            setattr(record, key, value)
        return Order(**record.dict())
    
    
    def delete(self, id_: str):
        self.session.delete(self._get(id_))