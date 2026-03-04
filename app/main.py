from fastapi import FastAPI, HTTPException, Query as Q, Path
from service.products import get_all_products
from schema.products import Product

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
    return product
