from pydantic import BaseModel
from datetime import date

class AcademicYearCreate(BaseModel):
    name: str
    start_date: date
    end_date: date
