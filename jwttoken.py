from jose import jwt
from datetime import datetime, timedelta
from decouple import config
import schemas
from jose import JWTError


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config(
        'SECRET_KEY'), algorithm=config('ALGORITHM'))
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, config('SECRET_KEY'),
                             algorithms=[config('ALGORITHM')])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        token_data = schemas.TokenData(username=username)
        print(token_data)
        return token_data
    except JWTError:
        raise credentials_exception
