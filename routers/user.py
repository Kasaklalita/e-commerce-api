from fastapi import APIRouter, Depends
from .. import hashing, schemas, o2auth, models, database

router = APIRouter(tags=['user'])
get_db = database.get_db


@router.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(o2auth.get_current_user)):
    return current_user


# @router.get("/users/me/items/")
# async def read_own_items(current_user: schemas.User = Depends(o2auth.get_current_user)):
#     return [{"item_id": "Foo", "owner": current_user.username}]


@router.post('/registration')
def user_registration(user: schemas.User, db: get_db = Depends()):
    user_info = user.dict(exclude_unset=True)
    user_info['password'] = hashing.Hash.get_password_hash(user_info['password'])
    new_user = models.User(**user_info)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
