from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_user_from_token
from app.models import Section
from datetime import datetime


router=APIRouter()

@router.post("/update-section/")
def update_section_by_admin(section_id: int = Form(...),new_name: str = Form(...),token: str = Form(...),db: Session = Depends(get_db)):
    user = get_user_from_token(token, db)

    if user.user_type != 1:
        return {"Status":0,"Message":"Only admin can update sections"}

    section = db.query(Section).filter(Section.section_id == section_id, Section.status == 1).first()
    if not section:
        return {"Status":0,"Message":"Section not found"}


    section.name = new_name
    section.m_by = user.id
    section.m_at = datetime.now()

    db.commit()
    db.refresh(section)

    return {"status": 1, "message": "Section updated successfully"}
