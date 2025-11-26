from fastapi import APIRouter
from pydantic import BaseModel
from budgetapp.db import conn, next_id

router = APIRouter()

class TransactionCreate(BaseModel):
    category_id: int
    amount: int
    month: str
    date: str

class TransactionResponse(BaseModel):
    id: int
    category_id: int
    amount: int
    name: str
    date: str

@router.post("/", response_model=TransactionResponse)
def create_transaction(tx: TransactionCreate):
    new_id = next_id("transactions")
    conn.execute(
        "INSERT INTO transactions (id, category_id, amount, name, date, deleted) VALUES (?, ?, ?, ?, ?, FALSE)",
        [new_id, tx.category_id, tx.amount, tx.name, tx.date],
    )

    # Update budget (optional: still use month derived from date)
    month = tx.date[:7]  # YYYY-MM
    row = conn.execute("""
        SELECT id, budgeted, spent, balance FROM budget_month_categories
        WHERE category_id = ? AND month = ?
    """, [tx.category_id, month]).fetchone()

    if row:
        spent = row[2] + (abs(tx.amount) if tx.amount < 0 else 0)
        balance = row[3] + tx.amount
        conn.execute("""
            UPDATE budget_month_categories
            SET spent = ?, balance = ?
            WHERE id = ?
        """, [spent, balance, row[0]])

    return {
        "id": new_id,
        "category_id": tx.category_id,
        "amount": tx.amount,
        "name": tx.name,
        "date": tx.date,
    }


@router.get("/", response_model=list[TransactionResponse])
def list_transactions():
    rows = conn.execute("SELECT id, category_id, amount, name, date FROM transactions WHERE deleted = FALSE").fetchall()
    return [{"id": r[0], "category_id": r[1], "amount": r[2], "name": r[3], "date": r[4]} for r in rows]
