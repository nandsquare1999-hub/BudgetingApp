from fastapi import APIRouter
from pydantic import BaseModel
from budgetapp.db import conn, next_id

router = APIRouter()

class CategoryCreate(BaseModel):
    name: str

class CategoryResponse(BaseModel):
    id: int
    name: str

@router.post("/", response_model=CategoryResponse)
def create_category(category: CategoryCreate):
    new_id = next_id("categories")
    conn.execute("INSERT INTO categories (id, name) VALUES (?, ?)", [new_id, category.name])
    return {"id": new_id, "name": category.name}

@router.get("/", response_model=list[CategoryResponse])
def list_categories():
    rows = conn.execute("SELECT id, name FROM categories").fetchall()
    return [{"id": r[0], "name": r[1]} for r in rows]
