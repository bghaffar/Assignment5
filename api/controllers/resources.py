from sqlalchemy.orm import Session
from ..models import models, schemas

# Create a new resource
def create(db: Session, resource: schemas.ResourceCreate):
    db_resource = models.Resource(
        name=resource.name,
        description=resource.description,
        quantity=resource.quantity
    )
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

# Read all resources
def read_all(db: Session):
    return db.query(models.Resource).all()

# Read one resource by ID
def read_one(db: Session, resource_id: int):
    return db.query(models.Resource).filter(models.Resource.id == resource_id).first()

# Update a resource
def update(db: Session, resource_id: int, resource: schemas.ResourceUpdate):
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    if db_resource:
        db_resource.name = resource.name
        db_resource.description = resource.description
        db_resource.quantity = resource.quantity
        db.commit()
        db.refresh(db_resource)
    return db_resource

# Delete a resource
def delete(db: Session, resource_id: int):
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    if db_resource:
        db.delete(db_resource)
        db.commit()
    return db_resource
