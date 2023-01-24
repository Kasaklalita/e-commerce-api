from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
import schemas
import models
import database
import o2auth
import secrets
from PIL import Image


router = APIRouter(tags=['Products'], prefix='/products')
get_db = database.get_db


@router.get('/')
async def get_products(skip: int = 0, limit: int = 100, db: get_db = Depends()):
    products = db.query(models.Product).all()
    return products[skip:limit]


@router.post("/")
async def add_new_product(product: schemas.Product, db: get_db = Depends(), user: schemas.User = Depends(o2auth.get_current_user)):
    product_business = db.query(models.Business).filter(
        models.Business.id == product.business_id).first()
    if not product_business:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect business_id")
    new_product = models.Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.get('/{id}')
async def get_product_details(id: int, db: get_db = Depends()):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    return product


@router.delete('/{id}')
async def delete_product(id: int, db: get_db = Depends(), user: schemas.User = Depends(o2auth.get_current_user)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if not product.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with id {id} not found")
    if product.first().business.owner.id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are not the owner of this product.")
    product.delete()
    db.commit()
    return 'deleted'


@router.put('/{id}')
async def update_product(id: int, request: schemas.Product, db: get_db = Depends(), user: schemas.User = Depends(o2auth.get_current_user)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if not product.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with id {id} not found.")
    if product.first().business.owner.id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are not the owner of this product.")
    try:
        product.update(request.dict())
        db.commit()
        return 'updated'
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Incorrect data.")


@router.post('/{id}/logo')
async def upload_product_logo(id: int, file: UploadFile, user: schemas.User = Depends(o2auth.get_current_user), db: get_db = Depends()):
    FILEPATH = './static/images'
    filename = file.filename
    extension = filename.split('.')[1]

    if extension not in ['png', 'jpg']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"File extension is not allowed.")

    token_name = secrets.token_hex(10) + '.' + extension
    generated_name = FILEPATH + '/' + token_name
    file_content = await file.read()

    updated_product = db.query(models.Product).filter(
        models.Product.id == id).first()
    if updated_product.business.owner.id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are not the owner of this product.")
    updated_product.update({'logo': generated_name[2:]})
    db.commit()

    with open(generated_name, 'wb') as file:
        file.write(file_content)

    # Resizing the image
    img = Image.open(generated_name)
    img = img.resize(size=(200, 200))
    img.save(generated_name)

    return 'success'
