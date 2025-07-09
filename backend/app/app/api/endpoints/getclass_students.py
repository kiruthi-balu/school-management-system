from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, master_access_user
from app.models import User, AcademicYearClass, AcademicYearStudent

router = APIRouter()

@router.post("/my-class-students/")
def get_my_class_students(user: User = Depends(master_access_user),db: Session = Depends(get_db)):
    if user.user_type != 3:
        return {"status": 0, "message": "Only class teachers can view their students"}

    my_class = db.query(AcademicYearClass).filter(AcademicYearClass.staff_id == user.id,AcademicYearClass.status == 1).first()

    if not my_class:
        return {"status": 0, "message": "No academic class assigned to you"}

    students = db.query(AcademicYearStudent).join(User, AcademicYearStudent.student_id == User.id).filter(AcademicYearStudent.ac_class_id == my_class.id,AcademicYearStudent.status == 1,User.status == 1).all()

    student_list = [{
        "student_id": student.student.id,
        "name": student.student.name,
        "email": student.student.email,
        "gender": student.student.gender,
        "dob": student.student.Dateofbirth,
        "aadhaar": student.student.aadhaar_num
    } for student in students]

    return {
        "status": 1,
        "message": "Students fetched successfully",
        "class_id": my_class.id,
        "class_teacher": user.name,
        "students": student_list
    }
