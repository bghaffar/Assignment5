from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import models, schemas


# Create a new order
def create(db: Session, order: schemas.OrderCreate):
    # Create a new instance of the Order model with the provided data
    db_order = models.Order(
        customer_name=order.customer_name,
        description=order.description
    )
    # Add the newly created Order object to the database session
    db.add(db_order)
    # Commit the changes to the database
    db.commit()
    # Refresh the Order object to ensure it reflects the current state in the database
    db.refresh(db_order)
    # Return the newly created Order object
    return db_order


# Get all orders
def read_all(db: Session):
    return db.query(models.Order).all()


# Get a single order by ID
def read_one(db: Session, order_id: int):
    # Query the database for the specific order by its ID
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


# Update an order by ID
def update(db: Session, order_id: int, order: schemas.OrderUpdate):
    # Query the database for the specific order to update
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    # Extract the update data from the provided 'order' object
    update_data = order.model_dump(exclude_unset=True)

    # Update the order fields
    for key, value in update_data.items():
        setattr(db_order, key, value)

    # Commit the changes to the database
    db.commit()
    db.refresh(db_order)

    # Return the updated order record
    return db_order


# Delete an order by ID
def delete(db: Session, order_id: int):
    # Query the database for the specific order to delete
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    # Delete the database record
    db.delete(db_order)
    # Commit the changes to the database
    db.commit()
    # Return a response with a status code indicating success (204 No Content)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
