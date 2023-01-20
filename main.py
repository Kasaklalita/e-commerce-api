from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import schemas
import models
from hashing import Hash
import database
from fastapi.security import (OAuth2PasswordBearer, OAuth2PasswordRequestForm)

app = FastAPI()
models.Base.metadata.create_all(database.engine)

db = database.get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


@app.post('/token')
async def generate_token(request_form: OAuth2PasswordRequestForm = Depends()):
    token = await token_gerenator(request_form.username, request_form.password)
    return {'acess_token': token, 'token_type': 'bearer'}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    return {'token': 'user_token'}


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
