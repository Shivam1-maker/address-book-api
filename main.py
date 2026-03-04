from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .database import engine, SessionLocal
from . import models, schemas, crud
from utils import calculate_distance
from logger import logger

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Address Book API")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create
@app.post("/addresses/", response_model=schemas.AddressResponse)
def create_address(address: schemas.AddressCreate, db: Session = Depends(get_db)):
    logger.info("Creating new address")
    return crud.create_address(db, address)

# Get All
@app.get("/addresses/", response_model=list[schemas.AddressResponse])
def list_addresses(db: Session = Depends(get_db)):
    return crud.get_all_addresses(db)

# Update
@app.put("/addresses/{address_id}", response_model=schemas.AddressResponse)
def update_address(address_id: int, address: schemas.AddressUpdate, db: Session = Depends(get_db)):
    db_address = crud.update_address(db, address_id, address)
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address

# Delete
@app.delete("/addresses/{address_id}")
def delete_address(address_id: int, db: Session = Depends(get_db)):
    db_address = crud.delete_address(db, address_id)
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    return {"message": "Address deleted successfully"}

# Nearby Search
@app.get("/addresses/nearby/", response_model=list[schemas.AddressResponse])
def get_nearby_addresses(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    distance_km: float = Query(..., gt=0),
    db: Session = Depends(get_db)
):
    addresses = crud.get_all_addresses(db)
    nearby = []

    for address in addresses:
        dist = calculate_distance(latitude, longitude, address.latitude, address.longitude)
        if dist <= distance_km:
            nearby.append(address)

    return nearby