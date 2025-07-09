from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from app.models import AcademicYearClass, User
from app.api.deps import get_db, master_access_user

router = APIRouter()

@router.post("/add-academic-class/")
def create_academic_class(ac_year_id: int = Form(...),standard_id: int = Form(...),section_id: int = Form(...),staff_id: int = Form(...),user: User = Depends(master_access_user),db: Session = Depends(get_db)):
    existing = db.query(AcademicYearClass).filter(AcademicYearClass.ac_year_id == ac_year_id,AcademicYearClass.standard_id == standard_id,AcademicYearClass.section_id == section_id,AcademicYearClass.status != -1).first()

    if existing:
        return {"status": 0, "message": "This class already exists for the academic year"}

    new_class = AcademicYearClass(
        ac_year_id=ac_year_id,
        standard_id=standard_id,
        section_id=section_id,
        staff_id=staff_id,
        c_by=user.id
    )
    db.add(new_class)
    db.commit()
    db.refresh(new_class)

    return {"status": 1, "message": "Academic class created successfully", "id": new_class.id}
