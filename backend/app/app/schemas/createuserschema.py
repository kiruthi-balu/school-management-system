from pydantic import BaseModel, EmailStr
from datetime import date

class CreateUser(BaseModel):
    name: str
    email: EmailStr
    password: str
    gender: str
    Dateofbirth: date
    aadhaar_num: str
    Father_name: str
    Mother_name: str
    guardian_name: str
    Address: str
    city: str
    pincode: str
    Father_pnum: str
    mother_pnum: str
    guardian_pnum: str
    blood_group: str
    religion: str
    nationality: str
    community: str
    is_hostel: str
    admission_date: date
    dummy:str
    user_type: int  
    c_by: int       