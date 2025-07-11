from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.api.deps import get_db, marks_view_access
from app.models import Mark, ExamAllocation, AcademicYearStudent, User, SubjectAllocation, Subject, Exam, AcademicYearClass, Standard, Section, AcademicYear

router = APIRouter()


#particular class rank

@router.post("/student-rank/")
def student_rank(exam_id: int = Query(..., description="Exam ID"),class_id: int = Query(..., description="Academic Year Class ID"),user: User = Depends(marks_view_access),db: Session = Depends(get_db)):
    
    exam_allo = db.query(ExamAllocation).filter(ExamAllocation.exam_id == exam_id,ExamAllocation.ac_class_id == class_id,ExamAllocation.status == 1).first()

    if not exam_allo:
        return {"Status": 0, "Message": "Exam not allocated to this class"}

    students = db.query(AcademicYearStudent).filter(
        AcademicYearStudent.ac_class_id == class_id,AcademicYearStudent.status == 1).all()

    if not students:
        return {"Status": 0, "Message": "No students found in the class"}

    student_scores = []

    for student in students:
        marks = db.query(Mark,Subject.name.label("subject_name")).join(SubjectAllocation, Mark.suballoc == SubjectAllocation.id).join(Subject, SubjectAllocation.subject_id == Subject.id).filter(Mark.acy_stud_id == student.id, Mark.exalloc == exam_allo.id).all()

        total_obtained = 0
        total_max = 0
        subject_details = []

        for mark_obj, subject_name in marks:
            subject_details.append({
                "subject": subject_name,
                "obtained_mark": mark_obj.obtained_mark,
                "max_mark": mark_obj.max_mark,
                "status": mark_obj.status
            })
            total_obtained += mark_obj.obtained_mark or 0
            total_max += mark_obj.max_mark or 0

        avg = round((total_obtained / total_max * 100), 2) if total_max else 0

        user_info = db.query(User).filter(User.id == student.student_id).first()
        class_info = db.query(AcademicYearClass).filter(AcademicYearClass.id == class_id).first()
        std = db.query(Standard).filter(Standard.id == class_info.standard_id).first()
        sec = db.query(Section).filter(Section.id == class_info.section_id).first()
        acy = db.query(AcademicYear).filter(AcademicYear.id == class_info.ac_year_id).first()
        exam = db.query(Exam).filter(Exam.id == exam_id).first()

        student_scores.append({
            "student_id": student.student_id,
            "student_name": user_info.name,
            "class": std.name,
            "section": sec.name,
            "academic_year": acy.name,
            "exam_name": exam.name,
            "subjects": subject_details,
            "total": total_obtained,
            "max_total": total_max,
            "average": avg
        })

    student_scores.sort(key=lambda x: x['total'], reverse=True)
    for i, score in enumerate(student_scores):
        score['rank'] = i + 1

    return {"Status": 1, "Result": student_scores}
