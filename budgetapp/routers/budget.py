from fastapi import APIRouter
from pydantic import BaseModel
from budgetapp.db import conn, next_id

router = APIRouter()

class BudgetAssign(BaseModel):
    category_id: int
    month: str
    amount: int

class BudgetResponse(BaseModel):
    id: int
    category_id: int
    month: str
    budgeted: int
    spent: int
    balance: int

@router.post("/assign", response_model=BudgetResponse)
def assign_budget(budget: BudgetAssign):
    new_id = next_id("budget_month_categories")
    conn.execute("""
        INSERT INTO budget_month_categories (id, category_id, month, budgeted, spent, balance)
        VALUES (?, ?, ?, ?, 0, ?)
    """, [new_id, budget.category_id, budget.month, budget.amount, budget.amount])
    row = conn.execute("SELECT * FROM budget_month_categories WHERE id = ?", [new_id]).fetchone()
    return dict(zip(["id","category_id","month","budgeted","spent","balance"], row))

@router.get("/{month}", response_model=list[BudgetResponse])
def get_budget(month: str):
    rows = conn.execute("SELECT * FROM budget_month_categories WHERE month = ?", [month]).fetchall()
    return [dict(zip(["id","category_id","month","budgeted","spent","balance"], r)) for r in rows]
