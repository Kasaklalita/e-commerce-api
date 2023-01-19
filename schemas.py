from pydantic import BaseModel
import datetime


class User(BaseModel):
    username: str
    email: str
    password: str
