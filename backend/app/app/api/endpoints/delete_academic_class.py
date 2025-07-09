from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.orm import Session
from app.models import AcademicYearClass, User
from app.api.deps import get_db, admin_only_user

router = APIRouter()

@router.post("/delete-academic-class/{class_id}")
def delete_academic_year_class(
    class_id: int = Path(...),
    user: User = Depends(admin_only_user),
    db: Session = Depends(get_db)
):
    cls = db.query(AcademicYearClass).filter(AcademicYearClass.id == class_id, AcademicYearClass.status != -1).first()
    if not cls:
        return {"Status":0,"Message":"Academic year class not found"}

    cls.status = -1
    cls.m_by = user.id

    db.commit()

    return {"status": 1, "message": "Academic year class deleted successfully"}
