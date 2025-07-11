from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, marks_view_access
from app.models import Mark,AcademicYearStudent,Exam,ExamAllocation,Subject,SubjectAllocation,User

from typing import Dict,Union

router = APIRouter()
# 2nd route view marks by class
@router.post("/view-marks-by-class/")
def view_marks_by_class(ac_class_id: int = Query(..., description="Academic Year Class ID"),db: Session = Depends(get_db),user: Union[User, Dict] = Depends(marks_view_access)):
    
    if isinstance(user, dict) and user.get("Status") == 0:
        return user
    
    results = (db.query(Mark.id.label("mark_id"),Mark.obtained_mark,Mark.max_mark,Mark.status.label("pass_fail"),AcademicYearStudent.id.label("student_acy_id"),
            AcademicYearStudent.student_id.label("student_id"),User.name.label("student_name"),Exam.name.label("exam_name"),Subject.name.label("subject_name"))
        .join(AcademicYearStudent, Mark.acy_stud_id == AcademicYearStudent.id).join(User, AcademicYearStudent.student_id == User.id)
        .join(ExamAllocation, Mark.exalloc == ExamAllocation.id).join(Exam, ExamAllocation.exam_id == Exam.id)
        .join(SubjectAllocation, Mark.suballoc == SubjectAllocation.id).join(Subject, SubjectAllocation.subject_id == Subject.id)
        .filter(AcademicYearStudent.ac_class_id == ac_class_id).order_by(User.name, Exam.name).all())

    if not results:
        return {"status": 0, "message": "No marks found for this class"}

    student_map: Dict[int, Dict] = {}

    for row in results:
        if row.student_id not in student_map:
            student_map[row.student_id] = {
                "student_id": row.student_id,
                "student_name": row.student_name,
                "exams": {}
            }

        if row.exam_name not in student_map[row.student_id]["exams"]:
            student_map[row.student_id]["exams"][row.exam_name] = []

        student_map[row.student_id]["exams"][row.exam_name].append({
            "subject": row.subject_name,
            "mark": row.obtained_mark,
            "max_mark": row.max_mark,
            "status": row.pass_fail
        })

    final_output = []
    for student_data in student_map.values():
        exams_list = []
        for exam_name, marks in student_data["exams"].items():
            exams_list.append({
                "exam": exam_name,
                "marks": marks
            })
        final_output.append({
            "student_id": student_data["student_id"],
            "student_name": student_data["student_name"],
            "exams": exams_list
        })

    return {"status": 1, "marks": final_output}
