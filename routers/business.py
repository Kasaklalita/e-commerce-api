from fastapi import APIRouter, Depends, HTTPException, status
import schemas
import models
import database

router = APIRouter(tags=['Businesses'], prefix='/businesses')
get_db = database.get_db


@router.get('/')
async def get_businesses(skip: int = 0, limit: int = 100, db: get_db = Depends()):
    businesses = db.query(models.Business).all()
    return businesses[skip:limit]


@router.post('/')
async def add_new_business(business: schemas.Business, db: get_db = Depends()):
    new_business = models.Business(**business.dict())
    db.add(new_business)
    db.commit()
    db.refresh(new_business)
    return new_business


@router.get('/{id}')
async def get_business_details(id: int, db: get_db = Depends()):
    business = db.query(models.Business).filter(
        models.Business.id == id).first()
    return business


@router.delete('/{id}')
async def delete_business(id: int, db: get_db = Depends()):
    business = db.query(models.Business).filter(models.Business.id == id)
    if not business.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Business with id {id} not found")
    business.delete()
    db.commit()
    return business


@router.put('/{id}')
def update_business(id: int, request: schemas.Business, db: get_db = Depends()):
    business = db.query(models.Business).filter(models.Business.id == id)
    if not business.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Business with id {id} not found')
    business.update(request.dict())
    db.commit()
    return 'updated'
