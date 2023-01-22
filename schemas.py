from pydantic import BaseModel
from datetime import date


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        orm_mode = True


class Product(BaseModel):
    name: str
    category: str
    original_price: float
    percentage_discount: int
    offer_expiration_data: date
    product_image: str
    # business_id: int

    class Config:
        orm_mode = True
