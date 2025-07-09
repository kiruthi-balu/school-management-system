from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class UserProfileOut(BaseModel):
    id: int
    name: str
    email: str
    gender: Optional[str]
    Dateofbirth: Optional[date]
    user_type: int
    admission_date: Optional[date]
    blood_group: Optional[str]
    nationality: Optional[str]
    Address: Optional[str]
    Father_name: Optional[str]
    Mother_name: Optional[str]
    guardian_name: Optional[str]
    Father_pnum: Optional[str]
    mother_pnum: Optional[str]
    guardian_pnum: Optional[str]

    class Config:
        orm_mode = True
