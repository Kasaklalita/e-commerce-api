from fastapi import FastAPI
import models
from database import engine

app = FastAPI()
models.Base.metadata.create_all(engine)


@app.get("/")
def root():
    return {"message": "Hello World"}
