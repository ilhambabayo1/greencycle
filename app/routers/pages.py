from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import app.crud as crud
from app.database import get_db
from app.schemas import RecycleItemCreate

router = APIRouter(tags=["pages"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request, category: str | None = None, db: Session = Depends(get_db)):
    items = crud.list_items(db, category)
    stats = crud.get_stats(db)
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "items": items,
            "stats": stats,
            "categories": crud.CATEGORIES,
            "selected_category": category,
        },
    )


@router.post("/items/create")
def create_item_form(
    title: str = Form(...),
    category: str = Form(...),
    weight_kg: float = Form(...),
    db: Session = Depends(get_db),
):
    crud.create_item(db, RecycleItemCreate(title=title, category=category, weight_kg=weight_kg))
    return RedirectResponse("/", status_code=303)


@router.post("/items/{item_id}/delete")
def delete_item_form(item_id: int, db: Session = Depends(get_db)):
    crud.delete_item(db, item_id)
    return RedirectResponse("/", status_code=303)


@router.get("/about", response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse(request, "about.html", {})
