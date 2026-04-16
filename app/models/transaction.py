from pydantic import BaseModel
from datetime import datetime

class Transaction(BaseModel):
    date: datetime
    details: str
    type: str
    amount: float
    balance: float
    category: str
    customer_id: str