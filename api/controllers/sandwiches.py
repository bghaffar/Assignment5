from fastapi import HTTPException, Depends, Response, status
from sqlalchemy.orm import Session
from typing import List
from ..models import models, schemas


from ..dependencies.database import get_db


# Create a new sandwich
def create(db: Session, sandwich: schemas.SandwichCreate):
    db_sandwich = models.Sandwich(
        name=sandwich.name,
        description=sandwich.description,
        price=sandwich.price,
    )
    db.add(db_sandwich)
    db.commit()
    db.refresh(db_sandwich)
    return db_sandwich

# Read all sandwiches
def read_all(db: Session) -> List[schemas.Sandwich]:
    return db.query(models.Sandwich).all()

# Read one sandwich by ID
def read_one(db: Session, sandwich_id: int) -> schemas.Sandwich:
    return db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id).first()

# Update a sandwich by ID
def update(db: Session, sandwich_id: int, sandwich: schemas.SandwichUpdate) -> schemas.Sandwich:
    db_sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id).first()
    if db_sandwich is None:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    update_data = sandwich.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_sandwich, key, value)
    db.commit()
    db.refresh(db_sandwich)
    return db_sandwich

# Delete a sandwich by ID
def delete(db: Session, sandwich_id: int) -> Response:
    db_sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id).first()
    if db_sandwich is None:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    db.delete(db_sandwich)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
