from sqlalchemy import Column, Integer, String, Float, DateTime
from .session import Base

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False, index=True) # Index for k-period lookups
    amount = Column(Float, nullable=False)
    # The calculated micro-investment amount after all rules
    final_remanent = Column(Float, default=0.0)

class TemporalRule(Base):
    """Stores the override logic for p (extra) and q (fixed) periods"""
    __tablename__ = "temporal_rules"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)  # 'p' for addition, 'q' for fixed override
    start_date = Column(DateTime, nullable=False, index=True)
    end_date = Column(DateTime, nullable=False, index=True)
    value = Column(Float, nullable=False) # 'fixed' amount or 'extra' amount