from app.api.deps import get_db,master_access_user
from app.models import *
from sqlalchemy.orm import Session
from fastapi import Depends,APIRouter



router= APIRouter()


@router.post("/add-standard/")
def create_standard(Standard_name: str,user: User = Depends(master_access_user),db: Session = Depends(get_db)):
    standard = Standard(name=Standard_name, c_by=user.user_type)
    db.add(standard)
    db.commit()
    db.refresh(standard)
    return {"status": 1, "message": "Standard created successfully"}
