from typing import List, Dict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(title="Test22 API", version="0.1.0")


class ItemIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=300)


class Item(ItemIn):
    id: int


# In-memory store for demo purposes
db: Dict[int, Item] = {}
_id_seq: int = 0


@app.get("/status")
def status() -> dict:
    return {"status": "ok", "service": app.title, "version": app.version}


@app.post("/echo")
def echo(payload: dict) -> dict:
    return {"echo": payload}


@app.post("/items", response_model=Item, status_code=201)
def create_item(item: ItemIn) -> Item:
    global _id_seq
    _id_seq += 1
    new = Item(id=_id_seq, **item.dict())
    db[new.id] = new
    return new


@app.get("/items", response_model=List[Item])
def list_items() -> List[Item]:
    return list(db.values())


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    return db[item_id]


@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemIn) -> Item:
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    updated = Item(id=item_id, **item.dict())
    db[item_id] = updated
    return updated


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int) -> None:
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    del db[item_id]
    return None


# To run locally: uvicorn app.main:app --reload
