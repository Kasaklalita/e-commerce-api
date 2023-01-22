from fastapi import FastAPI
import models
import database
from routers import authentication, user, product, business
from fastapi.staticfiles import StaticFiles


models.Base.metadata.create_all(database.engine)

app = FastAPI()
app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(product.router)
app.include_router(business.router)
app.mount('/static', StaticFiles(directory='static'), name='static')
