from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import schemas
import models
from hashing import Hash
import database

app = FastAPI()
models.Base.metadata.create_all(database.engine)

db = database.get_db


@app.post('/registration')
def user_registration(user: schemas.User, db: Session = Depends(db)):
    user_info = user.dict(exclude_unset=True)
    user_info['password'] = Hash.bcrypt(user_info['password'])
    new_user = models.User(**user_info)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/")
def root():
    return {"message": "Hello World"}
