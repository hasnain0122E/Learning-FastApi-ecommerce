from fastapi import FastAPI, HTTPException, Query as Q, Path
from service.products import (
    get_all_products,
    add_product,
    remove_product,
    change_product,
)
from schema.products import Product, Product_Update
from uuid import uuid4, UUID
from datetime import datetime

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}


@app.get("/products")
def list_products(
    name: str = Q(
        default=None, min_length=3, max_length=50, description="Search products by name"
    ),
    sort_by_price: bool = Q(default=False, description="Sorting products by price"),
    order: str = Q(
        default="asc",
        description="Sorting products if sort_by_products is true, either asc or desc",
    ),
    limit: int = Q(
        default=1, ge=1, le=100, description="total number of products returned"
    ),
    page: int = Q(default=1, ge=1, description="Offset for pagination"),
):

    products = get_all_products()
    if name:
        searched_products = name.strip().lower()
        products = [p for p in products if searched_products in p["name"].lower()]

    if not products:
        raise HTTPException(
            status_code=404, detail=f"Cannot find the product name = {name}"
        )

    if sort_by_price:
        reverse = order == "desc"
        products = sorted(products, key=lambda p: p["price"], reverse=reverse)

    total = len(products)
    products = products[page - 1 : page - 1 + limit]

    return {"total_products": total, "limit": limit, "page": page, "Items": products}


@app.get("/products/{product_id}")
def get_product(
    product_id: str = Path(
        ...,
        min_length=36,
        max_length=36,
        description="The ID of the product to retrieve",
    ),
):
    products = get_all_products()
    for product in products:
        if product["id"] == product_id:
            return product

    raise HTTPException(status_code=404, detail="product not found!")


@app.post("/products", status_code=201)
def create_product(product: Product):
    product_dict = product.model_dump(mode="json")
    product_dict["id"] = str(uuid4())
    product_dict["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        add_product(product_dict)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return product_dict


@app.delete("/products/{product_id}")
def delete_product(product_id: UUID = Path(..., description="Product ID to delete")):
    try:
        res = remove_product(str(product_id))
        return res
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.put("/products/{product_id}")
def update_product(
    product_id: UUID = Path(..., description="Product ID to update"),
    payload: Product_Update = ...,
):
    try:
        update_product = change_product(
            str(product_id), payload.model_dump(mode="json", exclude_unset=True)
        )
        return update_product
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
