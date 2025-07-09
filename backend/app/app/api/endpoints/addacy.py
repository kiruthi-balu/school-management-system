from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from app.api.deps import get_db, master_access_user
from app.models import AcademicYear, User
from datetime import date

router = APIRouter()

@router.post("/add-academic-year/")
def create_academic_year(name: str = Form(...),user: User = Depends(master_access_user),db: Session = Depends(get_db)):
    
    existing = db.query(AcademicYear).filter(AcademicYear.name == name, AcademicYear.status != -1).first()
    if existing:
        return {"status": 0, "message": "Academic year already exists"}

    new_year = AcademicYear(
        name=name,
        c_by=user.id
    )
    db.add(new_year)
    db.commit()
    db.refresh(new_year)

    return {"status": 1, "message": "Academic year created successfully", "id": new_year.id}
