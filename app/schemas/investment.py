from pydantic import BaseModel
from typing import List, Optional

# Basic building blocks
class ExpenseInput(BaseModel):
    date: str
    amount: float

class EnrichedTransaction(BaseModel):
    date: str
    amount: float
    ceiling: float
    remanent: float

class PeriodRule(BaseModel):
    start: str
    end: str
    fixed: Optional[float] = 0.0
    extra: Optional[float] = 0.0

# 1. Schema for /transactions:parse
class ParseRequest(BaseModel):
    expenses: List[ExpenseInput]

# 2. Schema for /transactions:validator
class ValidatorRequest(BaseModel):
    wage: float
    transactions: List[EnrichedTransaction]

# 3. Schema for /returns:nps and /returns:index
class InvestmentRequest(BaseModel):
    age: int
    wage: float
    inflation: float
    q: List[PeriodRule]
    p: List[PeriodRule]
    k: List[PeriodRule]
    transactions: List[ExpenseInput]