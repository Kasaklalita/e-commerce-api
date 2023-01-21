from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import jwtToken
import schemas
import models
from hashing import Hash
from decouple import config
import database
import authentication
from fastapi.security import (OAuth2PasswordBearer, OAuth2PasswordRequestForm)

app = FastAPI()
models.Base.metadata.create_all(database.engine)

db = database.get_db

# fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
#         "disabled": False,
#     }
# }


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: database.get_db = Depends()):
    user = authentication.authenticate_user(
        form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=int(config('ACCESS_TOKEN_EXPIRE_MINUTES')))
    access_token = jwtToken.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(authentication.get_current_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: schemas.User = Depends(authentication.get_current_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]


@app.post('/registration')
def user_registration(user: schemas.User, db: Session = Depends(db)):
    user_info = user.dict(exclude_unset=True)
    user_info['password'] = Hash.get_password_hash(user_info['password'])
    new_user = models.User(**user_info)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# @app.get("/")
# def root():
#     return {"message": "Hello World"}
