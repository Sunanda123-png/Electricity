from pydantic import BaseModel
from typing import Optional


class UserRegister(BaseModel):
    username: str
    password: str
    email: str
    address: str
    role: Optional[str] = "user"


class UserLogin(BaseModel):
    username: str
    password: str


class ConsumptionData(BaseModel):
    month: str
    units_consumed: int


class InvoiceRequest(BaseModel):
    month: str
