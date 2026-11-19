from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field


class ExpenseRequest(BaseModel):
    employee_id: str = Field(min_length=1)
    merchant: str = Field(min_length=1)
    amount: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    currency: Literal["EUR"] = "EUR"
    category: Literal["meals", "travel", "lodging", "supplies"]
    description: str = Field(min_length=1, max_length=500)
