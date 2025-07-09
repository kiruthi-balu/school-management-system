from fastapi import Depends,APIRouter
from app.api.deps import get_db,master_access_user
from app.models import *
from sqlalchemy.orm import Session


router= APIRouter()


@router.post("/add-subject/")
def create_subject(Subject_name: str,user: User = Depends(master_access_user),db: Session = Depends(get_db)):
    subject = Subject(name=Subject_name, c_by=user.user_type)
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return {"status": 1, "message": "Subject created successfully"}
