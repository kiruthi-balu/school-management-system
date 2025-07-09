from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_user_from_token
from app.models import Subject, SubjectAllocation
from fastapi import Header

router = APIRouter()

@router.post("/class-subjects/")
def get_subjects_by_class(ac_class_id: int = Query(..., description="Academic Year Class ID"),token: str = Header(...),db: Session = Depends(get_db)):

    user = get_user_from_token(token, db)

    if isinstance(user, dict) and user.get("Status") == 0:
        return user  

    subject_rows = (db.query(Subject.id, Subject.name).join(SubjectAllocation, Subject.id == SubjectAllocation.subject_id)
        .filter(SubjectAllocation.ac_class_id == ac_class_id,SubjectAllocation.status == 1).distinct().all())

    if not subject_rows:
        return {"status": 0, "message": "No subjects found for this class"}

    subjects = [{"subject_id": s.id, "subject_name": s.name} for s in subject_rows]

    return {
        "status": 1,
        "class_id": ac_class_id,
        "subjects": subjects
    }
