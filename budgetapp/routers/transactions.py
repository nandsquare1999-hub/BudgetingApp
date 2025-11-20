from fastapi import APIRouter
from pydantic import BaseModel
from budgetapp.db import conn, next_id

router = APIRouter()

class TransactionCreate(BaseModel):
    category_id: int
    amount: int
    month: str

class TransactionResponse(BaseModel):
    id: int
    category_id: int
    amount: int

@router.post("/", response_model=TransactionResponse)
def create_transaction(tx: TransactionCreate):
    new_id = next_id("transactions")
    conn.execute("INSERT INTO transactions (id, category_id, amount) VALUES (?, ?, ?)", [new_id, tx.category_id, tx.amount])

    # Update budget
    row = conn.execute("""
        SELECT id, budgeted, spent, balance FROM budget_month_categories
        WHERE category_id = ? AND month = ?
    """, [tx.category_id, tx.month]).fetchone()

    if row:
        spent = row[2] + (abs(tx.amount) if tx.amount < 0 else 0)
        balance = row[3] + tx.amount
        conn.execute("""
            UPDATE budget_month_categories
            SET spent = ?, balance = ?
            WHERE id = ?
        """, [spent, balance, row[0]])

    return {"id": new_id, "category_id": tx.category_id, "amount": tx.amount}

@router.get("/", response_model=list[TransactionResponse])
def list_transactions():
    rows = conn.execute("SELECT id, category_id, amount FROM transactions").fetchall()
    return [{"id": r[0], "category_id": r[1], "amount": r[2]} for r in rows]
