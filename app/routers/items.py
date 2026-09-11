from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import app.crud as crud
from app.database import get_db
from app.schemas import RecycleItemCreate, RecycleItemOut

router = APIRouter(prefix="/api/items", tags=["items"])


@router.get("", response_model=list[RecycleItemOut])
def read_items(category: str | None = None, db: Session = Depends(get_db)):
    return crud.list_items(db, category)


@router.get("/stats")
def read_stats(db: Session = Depends(get_db)):
    return crud.get_stats(db)


@router.post("", response_model=RecycleItemOut, status_code=201)
def create_item(data: RecycleItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, data)


@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    if not crud.delete_item(db, item_id):
        raise HTTPException(status_code=404, detail="Item not found")
