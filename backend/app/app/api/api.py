from fastapi import APIRouter
from .endpoints import userlogin, createuser,update_user, delete_user, list_user,logout
from .endpoints import getclass_students, viewprofile
from .endpoints import addacy,view_academic_year,delete_academic_year,update_ac_year
from .endpoints import  addacystudent, view_acy_students,update_acy_student,delete_acy_student
from .endpoints import addacyclass,view_academic_class,update_academic_class,delete_academic_class
from .endpoints import delete_standard, addstandard, update_standard, view_standard
from .endpoints import update_section,delete_section,addsection,view_section
from .endpoints import add_exam,view_exam,update_exam, delete_exam
from .endpoints import create_exam_allocation, update_exam_allocation, delete_exam_allocation, view_examallocation
from .endpoints import create_sub_allocation, update_sub_allocation, delete_sub_allocation, view_subjectallocation
from .endpoints import add_questionpaper
from .endpoints import addmark,viewmark,individual_mark, class_rank
from .endpoints import view_subject, addsubject, update_subject,delete_subject
from .endpoints import add_attendance, class_attendance_percentage, daily_attendance, individual_att_percentage
from .endpoints import add_timetable, view_staff_timetable,view_class_timetable,update_timetable,delete_timetable
from .endpoints import leave_request 
from .endpoints import fees_crud

api_router = APIRouter()


api_router.include_router(userlogin.router, tags=["Login"])
api_router.include_router(logout.router, tags=["Logout"])



api_router.include_router(createuser.router,tags=["User"])
api_router.include_router(update_user.router,tags=["User"])
api_router.include_router(delete_user.router,tags=["User"])
api_router.include_router(viewprofile.router,tags=["User"])
api_router.include_router(list_user.router,tags=["User"])

api_router.include_router(getclass_students.router,tags=["View"])
api_router.include_router(view_subject.router,tags=["View"])
api_router.include_router(view_examallocation.router,tags=["View"])
api_router.include_router(view_subjectallocation.router,tags=["View"])


api_router.include_router(add_attendance.router,tags=["Attendance"])
api_router.include_router(class_attendance_percentage.router,tags=["Attendance"])
api_router.include_router(daily_attendance.router,tags=["Attendance"])
api_router.include_router(individual_att_percentage.router,tags=["Attendance"])


api_router.include_router(add_questionpaper.router,tags=["Marks"])
api_router.include_router(addmark.router,tags=["Marks"])
api_router.include_router(viewmark.router,tags=["Marks"])
api_router.include_router(individual_mark.router,tags=["Marks"])
api_router.include_router(class_rank.router,tags=["Marks"])




api_router.include_router(addsubject.router,tags=["Subject"])
api_router.include_router(update_subject.router,tags=["Subject"])
api_router.include_router(delete_subject.router,tags=["Subject"])


api_router.include_router(addstandard.router,tags=["Standard"])
api_router.include_router(update_standard.router,tags=["Standard"])
api_router.include_router(delete_standard.router,tags=["Standard"])
api_router.include_router(view_standard.router,tags=["Standard"])


api_router.include_router(addsection.router,tags=["Section"])
api_router.include_router(update_section.router,tags=["Section"])
api_router.include_router(delete_section.router,tags=["Section"])
api_router.include_router(view_section.router,tags=["Section"])



api_router.include_router(addacy.router,tags=["AcademicYear"])
api_router.include_router(view_academic_year.router,tags=["AcademicYear"])
api_router.include_router(update_ac_year.router,tags=["AcademicYear"])
api_router.include_router(delete_academic_year.router,tags=["AcademicYear"])


api_router.include_router(addacyclass.router,tags=["Academic Year Class"])
api_router.include_router(view_academic_class.router,tags=["Academic Year Class"])
api_router.include_router(update_academic_class.router,tags=["Academic Year Class"])
api_router.include_router(delete_academic_class.router,tags=["Academic Year Class"])


api_router.include_router(addacystudent.router,tags=["Academic Year Student"])
api_router.include_router(view_acy_students.router,tags=["Academic Year Student"])
api_router.include_router(update_acy_student.router,tags=["Academic Year Student"])
api_router.include_router(delete_acy_student.router,tags=["Academic Year Student"])



api_router.include_router(add_exam.router,tags=["Exam"])
api_router.include_router(view_exam.router,tags=["Exam"])
api_router.include_router(update_exam.router,tags=["Exam"])
api_router.include_router(delete_exam.router,tags=["Exam"])


api_router.include_router(create_exam_allocation.router,tags=["Exam Allocation"])
api_router.include_router(update_exam_allocation.router,tags=["Exam Allocation"])
api_router.include_router(delete_exam_allocation.router,tags=["Exam Allocation"])


api_router.include_router(create_sub_allocation.router,tags=["Subject Allocation"])
api_router.include_router(update_sub_allocation.router,tags=["Subject Allocation"])
api_router.include_router(delete_sub_allocation.router,tags=["Subject Allocation"])

api_router.include_router(add_timetable.router,tags=["Time Table"])
api_router.include_router(view_class_timetable.router,tags=["Time Table"])
api_router.include_router(view_staff_timetable.router,tags=["Time Table"])
api_router.include_router(update_timetable.router,tags=["Time Table"])
api_router.include_router(delete_timetable.router,tags=["Time Table"])


api_router.include_router(leave_request.router,tags=["Leave Request"])
api_router.include_router(fees_crud.router,tags=["Fees Structure"])








