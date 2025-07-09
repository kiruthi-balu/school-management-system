from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, master_access_user
from app.models import Section, User

router = APIRouter()

@router.post("/view-sections/")
def view_sections(user: User = Depends(master_access_user), db: Session = Depends(get_db)):
    sections = db.query(Section).filter(Section.status == 1).all()

    if not sections:
        return {"status": 0, "message": "No sections found"}

    return {
        "status": 1,
        "data": [{"id": sec.id, "name": sec.name} for sec in sections]
    }
