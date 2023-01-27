from pydantic import BaseModel
from datetime import date
from typing import List, Union


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
    # username: str | None = None


class UserBase(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        orm_mode = True


class BusinessBase(BaseModel):
    name: str
    city: str
    region: str
    description: str

    class Config:
        orm_mode = True


class Product(BaseModel):
    name: str
    category: str
    original_price: float
    percentage_discount: int
    offer_expiration_data: date
    product_image: str
    business_id: int

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    businesses: List[BusinessBase] = []
    join_date: date
    profile_picture: str


class Business(BusinessBase):
    logo: str
    owner_id: int


class BusinessExtended(Business):
    products: List[Product] = []
