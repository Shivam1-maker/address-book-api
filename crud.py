from sqlalchemy.orm import Session
from . import models, schemas

def create_address(db: Session, address: schemas.AddressCreate):
    db_address = models.Address(**address.model_dump())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

def get_all_addresses(db: Session):
    return db.query(models.Address).all()

def get_address(db: Session, address_id: int):
    return db.query(models.Address).filter(models.Address.id == address_id).first()

def update_address(db: Session, address_id: int, address: schemas.AddressUpdate):
    db_address = get_address(db, address_id)
    if not db_address:
        return None

    for key, value in address.model_dump().items():
        setattr(db_address, key, value)

    db.commit()
    db.refresh(db_address)
    return db_address

def delete_address(db: Session, address_id: int):
    db_address = get_address(db, address_id)
    if not db_address:
        return None

    db.delete(db_address)
    db.commit()
    return db_address