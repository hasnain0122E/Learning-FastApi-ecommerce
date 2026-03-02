from fastapi import FastAPI, HTTPException, Query as Q
from service.products import get_all_products

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}


""" @app.get("/products")
def get_products():
    return get_all_products() """


@app.get("/products")
def list_products(
    name: str = Q(
        default=None, min_length=1, max_length=50, description="Search products by name"
    ),
):

    products = get_all_products()
    if name:
        search_product = name.strip().lower()
        products = [p for p in products if search_product in p["name"].lower()]

        if not products:
            raise HTTPException(
                status_code=404, detail=f"No products found matching '{name}'"
            )

        total = len(products)

    return {"total products": total, "products": products}
