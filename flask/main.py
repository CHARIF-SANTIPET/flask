from http.client import HTTPException

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import engine, Base, get_db
from .models import Item, Receiver
from .schema import (
    ItemCreate,
    ItemResponse,
    ReceiverCreate,
    ReceiverResponse,
    ItemWithReceiverResponse,
)

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/receivers/", response_model=list[ReceiverResponse])
def read_receivers_list(db: Session = Depends(get_db)) -> list[ReceiverResponse]:
    db_receivers = db.query(Receiver).all()
    if not db_receivers:
        raise HTTPException(status_code=404, detail="No receivers found")
    return db_receivers


@app.get("/receivers/{receiver_id}", response_model=ReceiverResponse)
def read_receivers(receiver_id: int, db: Session = Depends(get_db)) -> ReceiverResponse:
    db_receiver = db.query(Receiver).filter(Receiver.id == receiver_id).first()
    if db_receiver is None:
        raise HTTPException(status_code=404, detail="Receiver not found")
    return db_receiver


@app.get("/receivers/{receiver_id}/items", response_model=list[ItemResponse])
def read_receiver_items(
    receiver_id: int, db: Session = Depends(get_db)
) -> list[ItemResponse]:
    db_receiver = db.query(Receiver).filter(Receiver.id == receiver_id).first()
    if db_receiver is None:
        raise HTTPException(status_code=404, detail="Receiver not found")

    items = db_receiver.item
    if not items:
        raise HTTPException(status_code=404, detail="No items found for this receiver")

    return items


@app.post("/receiver/", response_model=ReceiverResponse)
async def create_receiver(
    receiver: ReceiverCreate, db: Session = Depends(get_db)
) -> ReceiverResponse:
    db_receiver = Receiver(**receiver.model_dump())
    db.add(db_receiver)
    db.commit()
    db.refresh(db_receiver)
    return db_receiver


@app.put("/receivers/{receiver_id}", response_model=ReceiverResponse)
async def update_receiver(
    receiver_id: int, receiver: ReceiverCreate, db: Session = Depends(get_db)
) -> ReceiverResponse:
    db_receiver = db.query(Receiver).filter(Receiver.id == receiver_id).first()
    if db_receiver is None:
        raise HTTPException(status_code=404, detail="Receiver not found")

    for key, value in receiver.model_dump().items():
        setattr(db_receiver, key, value)

    db.commit()
    db.refresh(db_receiver)
    return db_receiver


@app.delete("/receivers/{receiver_id}")
async def delete_receiver(receiver_id: int, db: Session = Depends(get_db)) -> dict:
    db_receiver = db.query(Receiver).filter(Receiver.id == receiver_id).first()
    if db_receiver is None:
        raise HTTPException(status_code=404, detail="Receiver not found")

    db.delete(db_receiver)
    db.commit()
    return {"receiver_id": receiver_id, "status": "deleted"}


@app.get("/items/", response_model=list[ItemResponse])
def read_items_list(db: Session = Depends(get_db)) -> list[ItemResponse]:
    db_items = db.query(Item).all()
    if not db_items:
        raise HTTPException(status_code=404, detail="No items found")
    return db_items


@app.get("/items/{item_id}", response_model=ItemWithReceiverResponse)
def read_item(item_id: int, db: Session = Depends(get_db)) -> ItemWithReceiverResponse:
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@app.post("/item/", response_model=ItemResponse)
async def create_item(item: ItemCreate, db: Session = Depends(get_db)) -> ItemResponse:
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int, item: ItemCreate, db: Session = Depends(get_db)
) -> ItemResponse:
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    for key, value in item.model_dump().items():
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)
    return db_item


@app.delete("/items/{item_id}")
async def delete_item(item_id: int, db: Session = Depends(get_db)) -> dict:
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(db_item)
    db.commit()
    return {"item_id": item_id, "status": "deleted"}
