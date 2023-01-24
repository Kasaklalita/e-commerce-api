from fastapi import FastAPI
import models
import database
from routers import authentication, user, product, business
from fastapi.staticfiles import StaticFiles
import uvicorn


models.Base.metadata.create_all(database.engine)

app = FastAPI()
app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(business.router)
app.include_router(product.router)
app.mount('/static', StaticFiles(directory='static'), name='static')


@app.get('/')
async def greetings():
    return 'Hello there! To test the endpoints, go to /docs'


if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")
