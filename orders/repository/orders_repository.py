from orders.orders_service.orders import Order
from orders.repository.models import OrderModel, OrderItemModel

from sqlalchemy.orm import Session

from orders.Web.api.schemas import OrderItemSchema

class OrdersRepository:
    
    def __init__(self, session: Session):
        self.session = session
        
    def add(self, items: list[OrderItemSchema], user_id: str):
        record = OrderModel(items=[OrderItemModel(**item) for item in items],
                            user_id=user_id
                            )
        self.session.add(record)
        return Order(**record.dict(), order_=record)
    
    def _get(self, id_: str, **filters):
        return (
            self.session.query(OrderModel)
            .filter(OrderModel.id == str(id_)).filter_by(**filters)
            .first()
        )
    
    def get(self, id_: str, **filters):
        order = self._get(id_,**filters)
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
        
        records = query.filter_by(**filters).limit(limit).all()
        return [Order(**record.dict()) for record in records]
    
    
    def update(self, id_, **payload):
        record = self._get(id_)
        if 'items' in payload:
            for item in record.items:
                self.session.delete(item)
            record.items = [
                OrderItemModel(**item) for item in payload.pop('items')
            ]
        for key, value in payload.items():
            setattr(record, key, value)
        return Order(**record.dict())
    
    
    def delete(self, id_: str):
        self.session.delete(self._get(id_))