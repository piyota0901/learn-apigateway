from datetime import datetime,timezone

ingredients = [
    {
        "id": "0f75a61f-b887-465f-b8ca-803ac33c9687",
        "name": "Milk",
        "stock": {
            "quantity": 100.00,
            "unit": "LITERS"
        },
        "supplier": "3d649ae5-1e60-4477-967e-1cad5268135e",
        "products": [],
        "lastUpdated": datetime.now(tz=timezone.utc)
    }   
]

products = [
    {
        "id": "63d120a6-661e-49cb-9850-e78d38d568d9",
        "name": "Walnut Bomb",
        "price": 37.00,
        "size": "MEDIUM",
        "available": False,
        "ingredients": [
            {
                "id": "0f75a61f-b887-465f-b8ca-803ac33c9687",
                "quantity": 100.00,
                "unit": "LITERS"
            }
        ],
        # Cake specific fields
        "hasFillings": False,
        "hasNutsToppingOptin": True,
        "lastUpdated": datetime.now(tz=timezone.utc)
    },
    {
        "id": "2733272c-692e-47a7-93c9-994398c79645",
        "name": "Cappuccino Star",
        "price": 12.50,
        "size": "SMALL",
        "available": True,
        "ingredients": [
            {
                "id": "4503b0d2-fdcd-446b-8bbe-8e290e64fb85",
                "quantity": 100.00,
                "unit": "LITERS"
            }
        ],
        "hasCreamOnTopOption": True,
        "hasServeOnIceOption": True,
        "lastUpdated": datetime.now(tz=timezone.utc)
    }
]