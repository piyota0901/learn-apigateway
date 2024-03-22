from copy import deepcopy
from itertools import islice
from ariadne import QueryType
from Web.data import ingredients, products

query = QueryType()

@query.field("allIngredients")
def resolve_all_ingredients(*_):
    return ingredients

@query.field("allProducts")
def resolve_all_products(*_):
    # products_with_ingredients = [deepcopy(product) for product in products]
    # for product in products_with_ingredients:
    #     for ingredient_recipe in product["ingredients"]:
    #         for ingredient in ingredients:
    #             if ingredient["id"] == ingredient_recipe["ingredient"]:
    #                 ingredient_recipe["ingredient"] = ingredient
    
    # return products_with_ingredients # 原材料が含まれた商品リストを返す
    return products

def get_page(items, items_per_page, page):
    page = (page - 1) # ゼロオリジンに変換
    start = page * items_per_page if page > 0 else page
    stop = start + items_per_page
    return list(islice(items, start, stop))

@query.field("products")
def resolve_products(*_, input=None):
    filtered = [product for product in products] # Copy the list
    if input is None:
        return filtered
    
    filtered = [
        product for product in filtered
        if product["available"] is input["available"]
    ]
    
    if input.get("minPrice") is not None:
        filtered = [
            product for product in filtered
            if product["price"] >= input["minPrice"]
        ]
    
    if input.get("maxPrice") is not None:
        filtered = [
            product for product in filtered
            if product["price"] <= input["maxPrice"]
        ]

    filtered.sort(
        key=lambda product: product.get(input["sortBy"], 0),
        reverse=input["sort"] == "DESCENDING"
    )
    
    return get_page(filtered, input["resultsPerPage"], input["page"])

