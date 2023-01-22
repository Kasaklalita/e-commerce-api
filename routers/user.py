from fastapi import APIRouter, Depends
import hashing
import schemas
import o2auth
import models
import database
from fastapi import File, UploadFile
import secrets
from PIL import Image

router = APIRouter(tags=['User'])
get_db = database.get_db


@router.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(o2auth.get_current_user)):
    return current_user


@router.post('/registration')
async def user_registration(user: schemas.UserBase, db: get_db = Depends()):
    user_info = user.dict(exclude_unset=True)
    user_info['password'] = hashing.Hash.get_password_hash(
        user_info['password'])
    new_user = models.User(**user_info)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post('/uploadfile/profile')
async def create_upload_file(file: UploadFile = File(...), user: schemas.User = Depends(o2auth.get_current_user)):
    FILEPATH = './static/images'
    filename = file.filename
    extension = filename.split('.')[1]

    if extension not in ['png', 'jpg']:
        return {'status': 'error', 'detail': 'File extension not allowed'}

    token_name = secrets.token_hex(10) + '.' + extension
    generated_name = FILEPATH + '/' + token_name
    file_content = await file.read()

    with open(generated_name, 'wb') as file:
        file.write(file_content)

    img = Image.open(generated_name)
    img = img.resize(size=(200, 200))
    img.save(generated_name)

    file.close()

    return {'success': True}


@router.post('/uploadfile/product/{id}')
async def create_upload_file(id: int, file: UploadFile, user: schemas.User = Depends(o2auth.get_current_user), db: get_db = Depends()):
    FILEPATH = './static/images'
    filename = file.filename
    extension = filename.split('.')[1]

    if extension not in ['png', 'jpg']:
        return {'status': 'error', 'detail': 'File extension not allowed'}

    token_name = secrets.token_hex(10) + '.' + extension
    generated_name = FILEPATH + '/' + token_name
    file_content = await file.read()

    with open(generated_name, 'wb') as file:
        file.write(file_content)

    # Resizing the image
    img = Image.open(generated_name)
    img = img.resize(size=(200, 200))
    img.save(generated_name)

    # product = db.query(models.Product).filter(models.Product.id == id).first()
    # business = db.query(models.Business).filter(
    #     models.Business.id == product.business_id)
    # print(business)
    return {'success': True}
