from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.models import TimeTable, SubjectAllocation, AcademicYearClass
from app.api.deps import get_db, master_access_user
from app.models import User

router = APIRouter()

@router.post("/view-timetable-by-class/")
def view_timetable_by_class(class_id: int = Query(..., description="Academic Class ID"),user: User = Depends(master_access_user),db: Session = Depends(get_db)):
    
    allocations = db.query(SubjectAllocation).filter(SubjectAllocation.ac_class_id == class_id,SubjectAllocation.status != -1).all()

    if not allocations:
        return {"Status":0, "Message":"No subject allocations found for this class"}

    sub_allo_ids = [alloc.id for alloc in allocations]

    timetable_entries = db.query(TimeTable).filter(TimeTable.sub_allo_id.in_(sub_allo_ids),TimeTable.status != -1).order_by(TimeTable.day, TimeTable.period).all()

    result = [{
        "timetable_id": t.id,
        "day": t.day,
        "period": t.period,
        "subject_allocation_id": t.sub_allo_id
    } for t in timetable_entries]

    return {"status": 1, "data": result}
