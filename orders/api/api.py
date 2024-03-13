from datetime import datetime
from typing import Optional
from uuid import UUID
import uuid

from fastapi import HTTPException
from starlette.responses import Response
from starlette import status

from app import app
from api.schemas import CreateOrderSchema, GetOrderSchema, GetOrdersSchema


ORDERS = []

@app.get("/orders", response_model=GetOrdersSchema)
def get_orders(cancelled: Optional[bool]=None, limit: Optional[int]=None):
    if cancelled is None and limit is None:
        return {"orders": ORDERS}
    
    query_set = [order for order in ORDERS]
    
    if cancelled is not None:
        if cancelled:
            query_set = [order for order in query_set if order["status"] == "cancelled"]
        else:
            query_set = [order for order in query_set if order["status"] != "cancelled"]
    
    if limit is not None and len(query_set) > limit:
        return {"orders": query_set[:limit]}
    
    return {"orders": query_set}

@app.post(
    "/orders", 
    status_code=status.HTTP_201_CREATED,
    response_model=GetOrderSchema
    )
def create_order(order_details: CreateOrderSchema):
    order = order_details.dict()
    order["id"] = uuid.uuid4()
    order["created"] = datetime.utcnow()
    order["status"] = "created"
    ORDERS.append(order)
    return order

@app.get("/orders/{order_id}", response_model=GetOrderSchema)
def get_order(order_id: UUID):
    # ORDERSからorder_idに一致するものを取得
    result = filter(lambda order: order["id"] == order_id, ORDERS)
    order = next(result, None)
    
    if order is None:
        raise HTTPException(
            status_code=404, detail=f"Order with ID {order_id} not found."
            )
    
    return order

@app.put("/orders/{order_id}", response_model=GetOrderSchema)
def update_order(order_id: UUID, order_details: CreateOrderSchema):
    # ORDERSからorder_idに一致するものを取得
    result = filter(lambda order: order["id"] == order_id, ORDERS)
    order = next(result, None)
    
    if order is None:
        raise HTTPException(
            status_code=404, detail=f"Order with ID {order_id} not found."
            )
    
    order.update(order_details.model_dump())
    return order

@app.delete(
    "/orders/{order_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response
)
def delete_order(order_id: UUID):
    # ORDERSからorder_idに一致するものを取得
    result = filter(lambda order: order["id"] == order_id, ORDERS)
    order = next(result, None)
    
    if order is None:
        raise HTTPException(
            status_code=404, detail=f"Order with ID {order_id} not found."
            )
    
    ORDERS.remove(order)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.post("/orders/{order_id}/cancel", response_model=GetOrderSchema)
def cancel_order(order_id: UUID):
    # ORDERSからorder_idに一致するものを取得
    result = filter(lambda order: order["id"] == order_id, ORDERS)
    order = next(result, None)
    
    if order is None:
        raise HTTPException(
            status_code=404, detail=f"Order with ID {order_id} not found."
            )
    
    order["status"] = "cancelled"
    return order

@app.post("/orders/{order_id}/pay", response_model=GetOrderSchema)
def pay_order(order_id: UUID):
    # ORDERSからorder_idに一致するものを取得
    result = filter(lambda order: order["id"] == order_id, ORDERS)
    order = next(result, None)
    
    if order is None:
        raise HTTPException(
            status_code=404, detail=f"Order with ID {order_id} not found."
            )
    
    order["status"] = "paid"
    return order
