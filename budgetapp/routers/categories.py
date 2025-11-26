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
    conn.execute(
        "INSERT INTO categories (id, name, deleted) VALUES (?, ?, FALSE)",
        [new_id, category.name]
    )
    return {"id": new_id, "name": category.name}

@router.get("/", response_model=list[CategoryResponse])
def list_categories():
    rows = conn.execute(
        "SELECT id, name FROM categories WHERE deleted = FALSE"
    ).fetchall()
    return [{"id": r[0], "name": r[1]} for r in rows]

@router.delete("/{id}")
def delete_category(id: int):
    conn.execute("UPDATE categories SET deleted = TRUE WHERE id = ?", [id])
    return {"message": f"Category {id} marked as deleted"}

@router.put("/restore/{id}")
def restore_category(id: int):
    conn.execute("UPDATE categories SET deleted = FALSE WHERE id = ?", [id])
    return {"message": f"Category {id} restored"}
