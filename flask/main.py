from fastapi import FastAPI

from pydantic import BaseModel

from .schema import ItemCreate, ItemResponse


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


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
