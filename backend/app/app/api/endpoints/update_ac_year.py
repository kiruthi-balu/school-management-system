# update_academic_year.py
from fastapi import APIRouter, Depends, Form, Path
from sqlalchemy.orm import Session
from app.models import AcademicYear, User
from app.api.deps import get_db, admin_only_user

router = APIRouter()

@router.post("/update-academic-year/{year_id}")
def update_academic_year(year_id: int = Path(...),name: str = Form(...),user: User = Depends(admin_only_user),db: Session = Depends(get_db)):
    
    year = db.query(AcademicYear).filter(AcademicYear.id == year_id, AcademicYear.status != -1).first()
    if not year:
        return {"Status":0,"Message":"Academic Year not found"}

    year.name = name
    year.m_by = user.id
    db.commit()
    db.refresh(year)

    return {"status": 1, "message": "Academic year updated successfully", "data": {"id": year.id, "name": year.name}}
