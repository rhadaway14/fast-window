from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Transaction(BaseModel):
    user_id: str
    transaction_id: str
    amount: float
    currency: str
    category: str
    type: str
    date: str
    notes: Optional[str] = None
