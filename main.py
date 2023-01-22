from fastapi import FastAPI, Depends
import models
import database
from fastapi.security import OAuth2PasswordBearer
from routers import authentication, user
from fastapi.staticfiles import StaticFiles


models.Base.metadata.create_all(database.engine)

app = FastAPI()
app.include_router(authentication.router)
app.include_router(user.router)
app.mount('/static', StaticFiles(directory='static'), name='static')
