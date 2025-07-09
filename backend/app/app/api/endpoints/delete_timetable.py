from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from app.models import TimeTable
from app.api.deps import get_db, master_access_user
from app.models import User

router = APIRouter()

@router.post("/delete-timetable/")
def delete_timetable(id: int = Form(...),user: User = Depends(master_access_user),db: Session = Depends(get_db)):
    
    timetable = db.query(TimeTable).filter(TimeTable.id == id, TimeTable.status != -1).first()
    
    if not timetable:
        return {"Status":0, "Message":"Timetable not found"}

    timetable.status = -1
    timetable.m_by = user.id
    db.commit()

    return {"status": 1, "message": "Timetable deleted successfully"}
