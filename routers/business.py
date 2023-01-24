from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
import schemas
import models
import database
import o2auth
import secrets
from PIL import Image

router = APIRouter(tags=['Businesses'], prefix='/businesses')
get_db = database.get_db


@router.get('/')
async def get_businesses(skip: int = 0, limit: int = 100, db: get_db = Depends()):
    businesses = db.query(models.Business).all()
    return businesses[skip:limit]


@router.post('/')
async def add_new_business(business: schemas.BusinessBase, db: get_db = Depends(), user: schemas.User = Depends(o2auth.get_current_user)):
    business_owner = db.query(models.User).filter(
        models.User.id == business.owner_id).first()
    if not business_owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect owner_id.")
    new_business = models.Business(**business.dict())
    try:
        db.add(new_business)
        db.commit()
        db.refresh(new_business)
        return new_business
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Business with this name already exists.")


@router.get('/{id}', response_model=schemas.Business)
async def get_business_details(id: int, db: get_db = Depends()):
    business = db.query(models.Business).filter(
        models.Business.id == id).first()
    return business


@router.delete('/{id}')
async def delete_business(id: int, db: get_db = Depends(), user: schemas.User = Depends(o2auth.get_current_user)):
    business = db.query(models.Business).filter(models.Business.id == id)
    if not business.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Business with id {id} not found.")
    owner_id = business.first().owner.id
    if owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are not the owner of this business.")
    business.delete()
    db.commit()
    return 'deleted'


@router.put('/{id}')
def update_business(id: int, request: schemas.BusinessBase, db: get_db = Depends(), user: schemas.User = Depends(o2auth.get_current_user)):
    business = db.query(models.Business).filter(models.Business.id == id)
    if not business.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Business with id {id} not found.')
    owner_id = business.first().owner.id
    if owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are not the owner of this business.")
    try:
        business.update(request.dict())
        db.commit()
        return 'updated'
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Incorrect data.")


@router.post('/{id}/logo')
async def upload_business_logo(id: int, file: UploadFile, user: schemas.User = Depends(o2auth.get_current_user), db: get_db = Depends()):
    FILEPATH = './static/images'
    filename = file.filename
    extension = filename.split('.')[1]

    if extension not in ['png', 'jpg']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"File extension is not allowed.")

    token_name = secrets.token_hex(10) + '.' + extension
    generated_name = FILEPATH + '/' + token_name
    file_content = await file.read()

    updated_business = db.query(models.Business).filter(
        models.Business.id == id).first()
    if updated_business.owner.id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are not the owner of this business.")
    updated_business.update({'logo': generated_name[2:]})
    db.commit()

    with open(generated_name, 'wb') as file:
        file.write(file_content)

    # Resizing the image
    img = Image.open(generated_name)
    img = img.resize(size=(200, 200))
    img.save(generated_name)

    return 'success'
