from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Literal
from datetime import datetime

class UserBase(BaseModel):
    name: str = Field(..., examples=["Asha Gupta"])
    email: EmailStr = Field(..., examples=["asha@example.com"])
    phone: str = Field(..., examples=["+91-9876543210"])

class UserCreate(UserBase):
    pass

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    wallet_balance: float

    class Config:
        from_attributes = True

class WalletAdjustIn(BaseModel):
    mode: Literal["delta", "set"] = Field("delta", description="delta: add/subtract amount; set: set absolute balance")
    amount: float = Field(..., description="Use positive to credit, negative to debit in delta mode; absolute value in set mode")
    description: Optional[str] = Field(default=None, examples=["Top-up via UPI", "Manual correction"])

class TransactionOut(BaseModel):
    id: int
    user_id: int
    amount: float
    type: str
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
