from fastapi import APIRouter
from budgetapp.db import conn, next_id

router = APIRouter()

@router.post("/{month}/rollover")
def rollover_budget(month: str, next_month: str):
    rows = conn.execute("SELECT category_id, budgeted, spent FROM budget_month_categories WHERE month = ?", [month]).fetchall()
    for r in rows:
        category_id, budgeted, spent = r
        rollover = budgeted - spent
        existing = conn.execute("SELECT id, balance FROM budget_month_categories WHERE category_id = ? AND month = ?", [category_id, next_month]).fetchone()
        if existing:
            conn.execute("UPDATE budget_month_categories SET balance = balance + ? WHERE id = ?", [rollover, existing[0]])
        else:
            new_id = next_id("budget_month_categories")
            conn.execute("""
                INSERT INTO budget_month_categories (id, category_id, month, budgeted, spent, balance)
                VALUES (?, ?, ?, 0, 0, ?)
            """, [new_id, category_id, next_month, rollover])
    return {"message": f"Rollover from {month} to {next_month} complete"}
