from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_user_from_token
from app.models import Section
from datetime import datetime


router=APIRouter()

@router.post("/delete-section/")
def delete_section_by_admin(section_id: int = Form(...),token: str = Form(...),db: Session = Depends(get_db)):
    
    
    user = get_user_from_token(token, db)

    if user.user_type != 1:
        return {"Status":0, "Message":"Only admin can delete sections"}


    section = db.query(Section).filter(Section.section_id == section_id, Section.status == 1).first()
    if not section:
        return {"Status":0, "Message":"No Section Found"}


    section.status = -1
    section.m_by = user.id
    section.m_at = datetime.now()

    db.commit()

    return {"status": 1, "message": "Section deleted successfully"}
