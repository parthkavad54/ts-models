from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    email: EmailStr
    password_hash: str
    role: str
    department: Optional[str] = None
    otp: Optional[str] = None
