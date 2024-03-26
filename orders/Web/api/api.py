from datetime import datetime
from typing import Optional
from uuid import UUID
import uuid

from fastapi import HTTPException
from starlette.responses import Response
from starlette.requests import Request
from starlette import status

from orders.Web.app import app
from orders.Web.api.schemas import CreateOrderSchema, GetOrderSchema, GetOrdersSchema

from orders.orders_service.exceptions import OrderNotFoundError
from orders.orders_service.orders_service import OrdersService
from orders.orders_service.orders import Order
from orders.repository.orders_repository import OrdersRepository
from orders.repository.unit_of_work import UnitOfWork
from orders.Web.app import app
from orders.Web.api.schemas import (
    GetOrderSchema,
    CreateOrderSchema,
    GetOrdersSchema
)


@app.get("/orders", response_model=GetOrdersSchema)
def get_orders(
    request: Request,
    cancelled: Optional[bool]=None, 
    limit: Optional[int]=None
    ):
    with UnitOfWork() as uow:
        repo = OrdersRepository(session=uow.session)
        orders_service = OrdersService(orders_repository=repo)
        results = orders_service.list_orders(limit=limit, cancelled=cancelled, user_id=request.state.user_id)
        
        for result in results:
            print("result: ", result.dict())
    return {"orders": [result.dict() for result in results]}

@app.post(
    "/orders", 
    status_code=status.HTTP_201_CREATED,
    response_model=GetOrderSchema
    )
def create_order(
    request: Request,
    payload: CreateOrderSchema
    ):
    with UnitOfWork() as uow:
        repo = OrdersRepository(session=uow.session)
        orders_service = OrdersService(orders_repository=repo)
        order: CreateOrderSchema = payload.model_dump()["order"]
        for item in order:
            item["size"] = item["size"].value
        
        # 注文を実行
        order: Order = orders_service.place_order(items=order, user_id=request.state.user_id)
        uow.commit()
        return_payload = order.dict()
        return return_payload

@app.get("/orders/{order_id}", response_model=GetOrderSchema)
def get_order(
    request: Request,
    order_id: UUID
    ):
    try:
        with UnitOfWork() as uow:
            repo = OrdersRepository(session=uow.session)
            orders_service = OrdersService(orders_repository=repo)
            order = orders_service.get_order(
                                    order_id=order_id,
                                    user_id=request.state.user_id
                                    )
            return order.dict()
    except OrderNotFoundError:
        raise HTTPException(
            status_code=404, detail=f"Order with ID {order_id} not found."
        )

@app.put("/orders/{order_id}", response_model=GetOrderSchema)
def update_order(
    request: Request,
    order_id: UUID, 
    order_details: CreateOrderSchema
    ):
    try:
        with UnitOfWork() as uow:
            repo = OrdersRepository(session=uow.session)
            orders_service = OrdersService(orders_repository=repo)
            order = order_details.model_dump()["order"]
            for item in order:
                item["size"] = item["size"].value
            order = orders_service.update_order(
                            order_id=order_id, 
                            items=order, 
                            user_id=request.state.user_id
                    )
            uow.commit()
        return order.dict()
    
    except OrderNotFoundError:
        raise HTTPException(
            status_code=404, detail=f"Order with ID {order_id} not found."
        )

@app.delete(
    "/orders/{order_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response
)
def delete_order(
    request: Request,
    order_id: UUID
    ):
    try:
        with UnitOfWork() as uow:
            repo = OrdersRepository(session=uow.session)
            orders_service = OrdersService(orders_repository=repo)
            orders_service.delete_order(order_id=order_id, user_id=request.state.user_id)
            uow.commit()
        return 
    except OrderNotFoundError:
        raise HTTPException(
            status_code=404, detail=f"Order with ID {order_id} not found."
        )

@app.post("/orders/{order_id}/cancel", response_model=GetOrderSchema)
def cancel_order(
    request: Request,
    order_id: UUID
    ):
    try:
        with UnitOfWork() as uow:
            repo = OrdersRepository(session=uow.session)
            orders_service = OrdersService(orders_repository=repo)
            order = orders_service.cancel_order(order_id=order_id, user_id=request.state.user_id)
            uow.commit()
        return order.dict()
    except OrderNotFoundError:
        raise HTTPException(
            status_code=404, detail=f"Order with ID {order_id} not found."
        )

@app.post("/orders/{order_id}/pay", response_model=GetOrderSchema)
def pay_order(
    request: Request,
    order_id: UUID
    ):
    try:
        with UnitOfWork() as uow:
            repo = OrdersRepository(session=uow.session)
            orders_service = OrdersService(orders_repository=repo)
            order = orders_service.pay_order(order_id=order_id, user_id=request.state.user_id)
            uow.commit()
        return order.dict()
    except OrderNotFoundError:
        raise HTTPException(
            status_code=404, detail=f"Order with ID {order_id} not found."
        )
