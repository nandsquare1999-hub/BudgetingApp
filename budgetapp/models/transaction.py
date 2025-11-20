from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from budgetapp.db import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    amount = Column(Integer, nullable=False)  # negative = spending, positive = income
    date = Column(DateTime, server_default=func.now())
