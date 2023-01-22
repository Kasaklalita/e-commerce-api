from fastapi import FastAPI, Depends
import models
import database
from fastapi.security import OAuth2PasswordBearer
from routers import authentication, user

models.Base.metadata.create_all(database.engine)

app = FastAPI()
app.include_router(authentication.router)
app.include_router(user.router)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# @app.get("/")
# def root():
#     return {"message": "Hello World"}
