from datetime import datetime
from uuid import UUID

from starlette.responses import Response
from starlette import status

from app import app
from api.schemas import CreateOrderSchema, GetOrderSchema, GetOrdersSchema


orders = [
            {
                'id': 'a173fb93-ef2a-468d-aa92-240de4fac896',
                'status': "delivered",
                'created': datetime.utcnow(),
                "order": [
                    {
                        'product': 'cappuccino',
                        'size': 'medium',
                        'quantity': 1,
                    }
                ]
            }
        ]

@app.get("/orders", response_model=GetOrdersSchema)
def get_orders():
    return {"orders": orders}

@app.post(
    "/orders", 
    status_code=status.HTTP_201_CREATED,
    response_model=GetOrderSchema
    )
def create_order(order_details: CreateOrderSchema):
    return orders

@app.get("/orders/{order_id}")
def get_order(order_id: UUID):
    return orders

@app.put("/orders/{order_id}")
def update_order(order_id: UUID, order_details: CreateOrderSchema):
    return orders

@app.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: UUID):
    return Response(status_code=status.HTTP_204_NO_CONTENT.value)

@app.post("/orders/{order_id}/cancel")
def cancel_order(order_id: UUID):
    return orders

@app.post("/orders/{order_id}/pay")
def pay_order(order_id: UUID):
    return orders
