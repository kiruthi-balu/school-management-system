from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import AcademicYear, User
from app.api.deps import get_db, master_access_user

router = APIRouter()

@router.post("/view-academic-years/")
def view_academic_years(user: User = Depends(master_access_user), db: Session = Depends(get_db)):
    years = db.query(AcademicYear).filter(AcademicYear.status != -1).all()
    if not years:
        return {"status": 0, "message": "No academic years found"}
    
    return {
        "status": 1,
        "data": [
            {
                "id": y.id,
                "name": y.name,
                "status": y.status,
                "created_at": y.c_at,
                "modified_at": y.m_at
            }
            for y in years
        ]
    }
