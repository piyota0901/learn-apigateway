from uuid import UUID
from orders.orders_service.exceptions import OrderNotFoundError
from orders.orders_service.orders import Order
from orders.repository.orders_repository import OrdersRepository

from orders.Web.api.schemas import OrderItemSchema

class OrdersService:
    def __init__(self, orders_repository: OrdersRepository):
        self.orders_repository = orders_repository
    
    
    def place_order(self, items: list[OrderItemSchema]):
        """注文する
        """
        return self.orders_repository.add(items=items)
    
    def get_order(self, order_id: str):
        order: Order = self.orders_repository.get(id_=order_id)
        if order is not None:
            return order
        raise OrderNotFoundError(f"Order with id {order_id} not found")
    
    def update_order(self, order_id: str, **payload):
        order = self.orders_repository.get(id_=order_id)
        if order is None:
            raise OrderNotFoundError(f"Order with id {order_id} not found")
        return self.orders_repository.update(order_id, **payload)
    
    def list_orders(self, **filters):
        limit = filters.pop("limit", None)
        return self.orders_repository.list(limit, **filters)
    
    def pay_order(self, order_id: str):
        order: Order = self.orders_repository.get(id_=order_id)
        if order is None:
            raise OrderNotFoundError(f"Order with id {order_id} not found")
        
        order.pay()
        
        schedule_id = order.schedule()
        return self.orders_repository.update(
            id_=order_id,
            status="progress",
            schedule_id=schedule_id
        )
    
    def cancel_order(self, order_id: str):
        order = self.orders_repository.get(id_=order_id)
        if order is None:
            raise OrderNotFoundError(f"Order with id {order_id} not found")
        
        order.cancel()
        return self.orders_repository.update(order_id, status="canceled")
    
    
    def delete_order(self, order_id):
        order = self.orders_repository.get(id_=order_id)
        if order is None:
            raise OrderNotFoundError(f'Order with id {order_id} not found')
        return self.orders_repository.delete(order_id)