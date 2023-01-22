from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import schemas
import models
from hashing import Hash
import database
import authentication
from fastapi.security import OAuth2PasswordBearer
from routers import authentication

models.Base.metadata.create_all(database.engine)

app = FastAPI()
app.include_router(authentication.router)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



# @app.get("/")
# def root():
#     return {"message": "Hello World"}
