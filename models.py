from pydantic import BaseModel
from typing import Optional

class Receipt(BaseModel):
    vendor: str
    date: str
    amount: float
    category: Optional[str] = "Misc"
