from pydantic import BaseModel
import datetime


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
