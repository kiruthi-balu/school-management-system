from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, master_access_user
from app.models import Standard, User

router = APIRouter()

@router.post("/view-standards/")
def view_standards(user: User = Depends(master_access_user), db: Session = Depends(get_db)):
    standards = db.query(Standard).filter(Standard.status == 1).all()
    
    if not standards:
        return {"status": 0, "message": "No standards found"}

    return {
        "status": 1,
        "data": [
            {"id": std.id, "name": std.name}
            for std in standards
        ]
    }
