from fastapi import APIRouter, Depends, Form, HTTPException, Path
from sqlalchemy.orm import Session
from app.models import AcademicYearClass, User
from app.api.deps import get_db, admin_only_user

router = APIRouter()

@router.post("/update-academic-class/{class_id}")
def update_academic_class(class_id: int = Path(...),ac_year_id: int = Form(...),standard_id: int = Form(...),section_id: int = Form(...),staff_id: int = Form(...),user: User = Depends(admin_only_user),db: Session = Depends(get_db)):
    cls = db.query(AcademicYearClass).filter(AcademicYearClass.id == class_id, AcademicYearClass.status != -1).first()
    if not cls:
        return {"Status":0, "Message":"Academic year class not found"}
    
    cls.ac_year_id = ac_year_id
    cls.standard_id = standard_id
    cls.section_id = section_id
    cls.staff_id = staff_id
    cls.m_by = user.id

    db.commit()
    db.refresh(cls)

    return {"status": 1, "message": "Academic year class updated successfully", "id": cls.id}
