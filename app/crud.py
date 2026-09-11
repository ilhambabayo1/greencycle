from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import RecycleItem
from app.schemas import RecycleItemCreate

CATEGORIES = ["Plastic", "Paper", "Glass", "Metal", "E-Waste", "Organic"]
POINTS_PER_KG = {
    "Plastic": 10,
    "Paper": 5,
    "Glass": 8,
    "Metal": 12,
    "E-Waste": 20,
    "Organic": 3,
}


def list_items(db: Session, category: str | None = None) -> list[RecycleItem]:
    query = db.query(RecycleItem)
    if category:
        query = query.filter(RecycleItem.category == category)
    return query.order_by(RecycleItem.created_at.desc()).all()


def get_item(db: Session, item_id: int) -> RecycleItem | None:
    return db.get(RecycleItem, item_id)


def create_item(db: Session, data: RecycleItemCreate) -> RecycleItem:
    points = data.points or int(POINTS_PER_KG.get(data.category, 5) * data.weight_kg)
    item = RecycleItem(
        title=data.title, category=data.category, weight_kg=data.weight_kg, points=points
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def delete_item(db: Session, item_id: int) -> bool:
    item = db.get(RecycleItem, item_id)
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True


def get_stats(db: Session) -> dict:
    row = db.query(
        func.count(RecycleItem.id),
        func.coalesce(func.sum(RecycleItem.weight_kg), 0.0),
        func.coalesce(func.sum(RecycleItem.points), 0),
    ).one()
    return {
        "total_items": row[0],
        "total_weight_kg": float(row[1]),
        "total_points": int(row[2]),
    }
