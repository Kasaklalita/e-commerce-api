import schemas
from hashing import Hash
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from decouple import config
from jose import JWTError, jwt
import database
import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def get_user(username: str, db: database.get_db = Depends()):
    # if username in db:
    #     user_dict = db[username]
    #     return schemas.UserInDB(**user_dict)
    user = db.query(models.User).filter(
        models.User.username == username).first()
    return user


def authenticate_user(username: str, password: str, db: database.get_db = Depends()):
    user = get_user(username, db)
    if not user:
        return False
    if not Hash.verify_password(password, user.password):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme), db: database.get_db = Depends()):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, config('SECRET_KEY'),
                             algorithms=[config('ALGORITHM')])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username, db=db)
    if user is None:
        raise credentials_exception
    return user


# async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user
