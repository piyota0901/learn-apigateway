import uuid
from datetime import datetime, timezone
from ariadne import MutationType
from Web.data import products

mutation = MutationType()

@mutation.field("addProduct")
def resolve_add_product(*_, name, type, input):
    product = {
        "id": uuid.uuid4(),
        "name": name,
        "available": input.get("available", False),
        "ingredients": input.get("ingredients", []),
        "lastUpdated": datetime.now(timezone.utc),
    }
    if type== "cake":
        product.update({
            "hasFillings": input["hasFillings"],
            "hasNutsToppingOption": input["hasNutsToppingOption"]
        })
    else:
        product.update({
            "hasCreamOnTopOption": input["hasCreamOnTopOption"],
            "hasServeOnIceOption": input["hasServeOnIceOption"]
        })
    products.append(product)
    return product