from sqlalchemy import Column, Integer, String, ForeignKey
from budgetapp.db import Base

class BudgetMonthCategory(Base):
    __tablename__ = "budget_month_categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    month = Column(String, nullable=False)  # e.g. "2025-11"
    budgeted = Column(Integer, default=0)
    spent = Column(Integer, default=0)
    balance = Column(Integer, default=0)
