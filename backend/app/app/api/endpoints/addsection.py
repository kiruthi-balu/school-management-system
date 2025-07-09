from app.api.deps import get_db,master_access_user
from app.models import *
from sqlalchemy.orm import Session
from fastapi import Depends,APIRouter


router= APIRouter()


@router.post("/add-section/")
def create_section(Section_name: str,user: User = Depends(master_access_user),db: Session = Depends(get_db)):
    section = Section(name=Section_name, c_by=user.user_type)
    db.add(section)
    db.commit()
    db.refresh(section)
    return {"status": 1, "message": "Section created successfully"}
