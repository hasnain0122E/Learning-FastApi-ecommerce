from pydantic import BaseModel, Field
from typing import Annotated, Literal
from uuid import UUID


class Product(BaseModel):
    id: UUID
    sku: Annotated[
        str,
        Field(
            min_length=6,
            max_length=20,
            description="The SKU of the product, must be between 6 and 20 characters",
            examples=["XIAO-359GB-0100", "REAL-135GB-1201"],
        ),
    ]
    name: Annotated[
        str,
        Field(
            min_length=3,
            max_length=50,
            description="The name of the product",
            examples=["Xiaomi 11T Pro", "Realme GT Neo 3"],
        ),
    ]
    description: Annotated[
        str, Field(max_length=200, description="The description of the product")
    ]
    category: Annotated[
        str,
        Field(
            min_length=3,
            max_length=30,
            description="The category of the product",
            examples=["Smartphone", "Laptop", "Headphones"],
        ),
    ]
    brand: Annotated[
        str,
        Field(
            min_length=2,
            max_length=30,
            description="The brand of the product",
            examples=["Xiaomi", "Realme", "Apple"],
        ),
    ]
    price: Annotated[
        float,
        Field(
            gt=0,
            description="The price of the product, must be positive",
            examples=[299.99, 499.99],
        ),
    ]
    currency: Literal["INR"] = "INR"
    discount_percentage: Annotated[
        int,
        Field(
            ge=0,
            le=90,
            description="The discount percentage for the product, must be between 0 and 90",
        ),
    ]
    stock: Annotated[
        int,
        Field(
            ge=0, description="The stock quantity of the product, must be non-negative"
        ),
    ]
    is_active: Annotated[
        bool, Field(description="Indicates whether the product is active or not")
    ]
    rating: Annotated[
        float,
        Field(
            ge=0, le=5, description="The rating of the product, must be between 0 and 5"
        ),
    ]
