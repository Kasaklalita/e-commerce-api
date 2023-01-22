from fastapi import APIRouter, Depends, HTTPException, status
import schemas
import models
import database


router = APIRouter(tags=['Products'], prefix='/products')
get_db = database.get_db


@router.get('/')
async def get_products(skip: int = 0, limit: int = 100, db: get_db = Depends()):
    products = db.query(models.Product).all()
    return products[skip:limit]


@router.post("/")
async def add_new_product(product: schemas.Product, db: get_db = Depends()):
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
async def delete_product(id: int, db: get_db = Depends()):
    product = db.query(models.Product).filter(models.Product.id == id)
    if not product.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with id {id} not found")
    product.delete()
    db.commit()
    return 'deleted'


@router.put('/{id}')
async def update_product(id: int, request: schemas.Product, db: get_db = Depends()):
    product = db.query(models.Product).filter(models.Product.id == id)
    if not product.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with id {id} not found")
    product.update(request.dict())
    db.commit()
    return 'updated'
