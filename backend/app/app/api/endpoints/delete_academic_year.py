from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from app.models import AcademicYear, User
from app.api.deps import get_db, admin_only_user

router = APIRouter()

@router.post("/delete-academic-year/{year_id}")
def delete_academic_year(year_id: int = Path(...),user: User = Depends(admin_only_user),db: Session = Depends(get_db)):
    
    year = db.query(AcademicYear).filter(AcademicYear.id == year_id, AcademicYear.status != -1).first()
    if not year:
        return {"Status":0,"Message":"Academic year not found"}

    year.status = -1
    year.m_by = user.id
    db.commit()

    return {"status": 1, "message": "Academic year deleted successfully"}
