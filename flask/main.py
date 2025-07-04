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


@app.get("/reseivers/", response_model=ReceiverResponse)
def read_receivers(db: Session = Depends(get_db)) -> list[ReceiverResponse]:
    db_receiver = db.query(Receiver).all()
    return db_receiver


@app.post("/receiver/", response_model=ReceiverResponse)
async def create_receiver(
    receiver: ReceiverCreate, db: Session = Depends(get_db)
) -> ReceiverResponse:
    db_receiver = Receiver(**receiver.model_dump())
    db.add(db_receiver)
    db.commit()
    db.refresh(db_receiver)
    return db_receiver


@app.get("/items/{item_id}")
def read_item(item_id: int, item: ItemResponse) -> dict:
    return {"item_id": item_id}


@app.post("/items/")
async def create_item(item: ItemCreate) -> ItemCreate:
    return {"item": item}


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: ItemCreate) -> ItemCreate:
    return {"item_id": item_id, "item": item}


@app.delete("/items/{item_id}")
async def delete_item(item_id: int) -> dict:
    return {"item_id": item_id, "status": "deleted"}
