from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from app.models import TimeTable, SubjectAllocation
from app.api.deps import get_db, master_access_user
from app.models import User

router = APIRouter()

@router.post("/add-timetable/")
def add_timetable(sub_allo_id: int = Form(...),day: str = Form(...),period: int = Form(...),user: User = Depends(master_access_user),db: Session = Depends(get_db)):


    subject_allo = db.query(SubjectAllocation).filter(SubjectAllocation.id == sub_allo_id,SubjectAllocation.status == 1).first()

    if not subject_allo:
        return {"Status":0, "Message":"Subject allocation not found."}

    new_tt = TimeTable(
        sub_allo_id=sub_allo_id,
        day=day,
        period=period,
        c_by=user.id
    )

    db.add(new_tt)
    db.commit()
    db.refresh(new_tt)

    return {
        "status": 1,
        "message": "Timetable added successfully",
        "data": {
            "id": new_tt.id,
            "sub_allo_id": new_tt.sub_allo_id,
            "day": new_tt.day,
            "period": new_tt.period,
            "created_by": user.name
        }
    }
