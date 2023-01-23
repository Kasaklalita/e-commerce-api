from fastapi import APIRouter, Depends, HTTPException, status
import hashing
import schemas
import o2auth
import models
import database
from fastapi import File, UploadFile
import secrets
from PIL import Image

router = APIRouter(tags=['Users'], prefix='/users')
get_db = database.get_db


@router.get("/me", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(o2auth.get_current_user)):
    return current_user


@router.post('/')
async def create_user(user: schemas.UserBase, db: get_db = Depends()):
    user_info = user.dict(exclude_unset=True)
    user_info['password'] = hashing.Hash.get_password_hash(
        user_info['password'])
    new_user = models.User(**user_info)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.put('/{id}')
def update_user(id: int, request: schemas.UserBase, db: get_db = Depends()):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Business with id {id} not found.')
    try:
        user.update(request.dict())
        db.commit()
        return 'updated'
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Business with this name already exists.")


@router.post('/me/profile-picture')
async def upload_profile_picture(file: UploadFile = File(...), user: schemas.User = Depends(o2auth.get_current_user), db: get_db = Depends()):
    FILEPATH = './static/images'
    filename = file.filename
    extension = filename.split('.')[-1]

    if extension not in ['png', 'jpg']:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect file extension.")

    token_name = secrets.token_hex(10) + '.' + extension
    generated_name = FILEPATH + '/' + token_name
    file_content = await file.read()

    updated_user = db.query(models.User).filter(models.User.id == user.id)
    updated_user.update({'profile_picture': generated_name[2:]})
    db.commit()

    with open(generated_name, 'wb') as file:
        file.write(file_content)

    img = Image.open(generated_name)
    img = img.resize(size=(200, 200))
    img.save(generated_name)

    file.close()

    return {'success': True}
