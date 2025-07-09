from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.api.deps import get_db, get_user_from_token
from app.models import User, AcademicYearStudent, Mark, Exam, Subject, SubjectAllocation

router = APIRouter()

@router.post("/student/view-marks/")
def student_view_marks(token: str = Query(...), db: Session = Depends(get_db)):

    user = get_user_from_token(token, db)

    if isinstance(user, dict):
        return user
    if user.user_type != 6:
        return {"Status": 0, "Message": "Only students can view their marks"}

    student_acy = db.query(AcademicYearStudent).filter(AcademicYearStudent.student_id == user.id,AcademicYearStudent.status == 1).first()

    if not student_acy:
        return {"Status": 0, "Message": "Student not assigned to any academic year class"}

    results = db.query(Mark.id.label("mark_id"),Exam.name.label("exam_name"),Subject.name.label("subject_name"),Mark.obtained_mark,Mark.max_mark,Mark.status.label("pass_fail")).join(Exam, Mark.exalloc == Exam.id).join(SubjectAllocation, Mark.suballoc == SubjectAllocation.id).join(Subject, SubjectAllocation.subject_id == Subject.id).filter(Mark.acy_stud_id == student_acy.id).order_by(Exam.name, Subject.name).all()

    if not results:
        return {"Status": 0, "Message": "No marks found for this student"}

    exam_data = {}
    for row in results:
        exam_name = row.exam_name
        if exam_name not in exam_data:
            exam_data[exam_name] = []

        exam_data[exam_name].append({
            "mark_id": row.mark_id,
            "subject": row.subject_name,
            "obtained_mark": row.obtained_mark,
            "max_mark": row.max_mark,
            "status": row.pass_fail
        })

    return {
        "Status": 1,
        "student_id": user.id,
        "student_name": user.name,
        "marks_by_exam": exam_data
    }
