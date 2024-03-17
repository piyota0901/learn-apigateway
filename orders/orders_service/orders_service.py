from uuid import UUID
from orders.orders_service.exceptions import OrderNotFoundError
from orders.orders_service.orders import Order
from repository.orders_repository import OrdersRepositry

from orders.Web.api.schemas import OrderItemSchema

class OrdersService:
    def __init__(self, orders_repository: OrdersRepositry):
        self.orders_repository = orders_repository
    
    
    def place_order(self, items: list[OrderItemSchema]):
        """注文する
        """
        return self.orders_repository.add(items=items)
    
    def get_order(self, order_id: str):
        order = self.orders_repository.get(order_id=order_id)
        if order is not None:
            return order
        raise OrderNotFoundError(f"Order with id {order_id} not found")
    
    def update_order(self, order_id: str, items: list[OrderItemSchema]):
        order = self.orders_repository.get(order_id=order_id)
        if order is not None:
            return self.orders_repository.update(order_id=order_id, items=items)
        
        return self.orders_repository.update(order_id, {"items": items})
    
    def list_orders(self, **filters):
        limit = filters.pop("limit", None)
        return self.orders_repository.list(limit, **filters)
    
    def pay_order(self, order_id: str):
        order: Order = self.orders_repository.get(order_id=order_id)
        if order is None:
            raise OrderNotFoundError(f"Order with id {order_id} not found")
        
        order.pay()
        
        schedule_id = order.schedule()
        return self.orders_repository.update(
            order_id,
            status="progress",
            schedule_id=schedule_id
        )
    
    def cancel_order(self, order_id: str):
        order = self.orders_repository.get(id_=order_id)
        if order is None:
            raise OrderNotFoundError(f"Order with id {order_id} not found")
        
        order.cancel()
        return self.orders_repository.update(order_id, status="canceled")