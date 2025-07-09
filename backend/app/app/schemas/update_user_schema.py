from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import date

class UpdateUser(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    gender: Optional[str]
    Dateofbirth: Optional[date]
    aadhaar_num: Optional[str]
    Father_name: Optional[str]
    Mother_name: Optional[str]
    guardian_name: Optional[str]
    Address: Optional[str]
    city: Optional[str]
    pincode: Optional[str]
    Father_pnum: Optional[str]
    mother_pnum: Optional[str]
    guardian_pnum: Optional[str]
    blood_group: Optional[str]
    religion: Optional[str]
    nationality: Optional[str]
    community: Optional[str]
    is_hostel: Optional[bool]
    admission_date: Optional[date]
    dummy: Optional[bool]
