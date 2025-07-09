from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import AcademicYearClass, User, Standard, Section
from app.api.deps import get_db, master_access_user

router = APIRouter()

@router.post("/view-academic-classes/")
def view_academic_year_classes(user: User = Depends(master_access_user),db: Session = Depends(get_db)):
    
    classes = db.query(AcademicYearClass).filter(AcademicYearClass.status != -1).all()
    
    if not classes:
        return {"status": 0, "message": "No academic year classes found"}
    
    data = []
    for cls in classes:
        data.append({
            "id": cls.id,
            "academic_year_id": cls.ac_year_id,
            "standard_id": cls.standard_id,
            "section_id": cls.section_id,
            "staff_id": cls.staff_id,
            "status": cls.status,
            "created_at": cls.c_at,
            "modified_at": cls.m_at
        })
    
    return {"status": 1, "data": data}
