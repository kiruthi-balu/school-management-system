from sqlalchemy import  Column, Integer, String, DateTime, ForeignKey,Date,func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from app.db.base_class import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name =  Column(String(100))
    email =  Column(String(100))
    password =   Column(String(100))
    gender = Column(String(20))
    Dateofbirth=Column(Date)
    aadhaar_num = Column(String(70))
    Father_name=Column(String(50))
    Mother_name=Column(String(50))
    guardian_name=Column(String(50))
    Address=Column(String(255))
    city = Column(String(30))
    pincode = Column(String(30))
    Father_pnum=Column(String(50))
    mother_pnum=Column(String(50))
    guardian_pnum=Column(String(50))
    blood_group = Column(String(30))
    religion = Column(String(30))
    nationality = Column(String(30))
    community = Column(String(30))
    is_hostel = Column(String(30))
    admission_date=Column(Date)
    dummy = Column(String(20))
    user_type = Column(TINYINT,default=6, comment="1:Admin, 2:Principal, 3:Teacher, 4:Office_staff, 5:Driver, 6:Student")

    status = Column(TINYINT, default=1, comment="1:Active,2:Inactive,-1:Deleted")
    c_by = Column(Integer, ForeignKey('user.id'), comment="Created by User ID")
    c_at = Column(DateTime, default=func.now())
    m_by = Column(Integer, ForeignKey('user.id'), comment="Modified by User ID")
    m_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Token relationship
    token = relationship("Apitoken", back_populates="user_data")

    # Reverse relationships
    created_standards = relationship("Standard", foreign_keys="Standard.c_by", back_populates="cby_standard")
    modified_standards = relationship("Standard", foreign_keys="Standard.m_by", back_populates="mby_standard")

    created_subjects = relationship("Subject", foreign_keys="Subject.c_by", back_populates="create_by")
    modified_subjects = relationship("Subject", foreign_keys="Subject.m_by", back_populates="modify_by")

    created_sections = relationship("Section", foreign_keys="Section.c_by", back_populates="create_by")
    modified_sections = relationship("Section", foreign_keys="Section.m_by", back_populates="modify_by")

    created_acy = relationship("AcademicYear", foreign_keys="AcademicYear.c_by", back_populates="acy_cby")
    modified_acy = relationship("AcademicYear", foreign_keys="AcademicYear.m_by", back_populates="acy_mby")


    # For AcademicYearClass
    assigned_classes = relationship("AcademicYearClass", foreign_keys="[AcademicYearClass.staff_id]", back_populates="staff")
    created_academic_classes = relationship("AcademicYearClass", foreign_keys="[AcademicYearClass.c_by]", back_populates="created_by")
    modified_academic_classes = relationship("AcademicYearClass", foreign_keys="[AcademicYearClass.m_by]", back_populates="modified_by")

    # For AcademicYearStudent
    enrolled_classes = relationship("AcademicYearStudent", foreign_keys="[AcademicYearStudent.student_id]", back_populates="student")
    created_academic_students = relationship("AcademicYearStudent", foreign_keys="[AcademicYearStudent.c_by]", back_populates="created_by")
    modified_academic_students = relationship("AcademicYearStudent", foreign_keys="[AcademicYearStudent.m_by]", back_populates="modified_by")


    # Inside User model

    student_attendance = relationship("Attendance", foreign_keys="[Attendance.user_id]", back_populates="student")
    created_attendance_entries = relationship("Attendance", foreign_keys="[Attendance.c_by]", back_populates="attendance_creator")
    modified_attendance_entries = relationship("Attendance", foreign_keys="[Attendance.m_by]",back_populates="attendance_modifier")

    # Inside User model

    leave_requests = relationship("LeaveRequest", foreign_keys="[LeaveRequest.user_id]", back_populates="student")
    leave_requests_created = relationship("LeaveRequest", foreign_keys="[LeaveRequest.c_by]", back_populates="leave_created_by")
    leave_requests_modified = relationship("LeaveRequest", foreign_keys="[LeaveRequest.m_by]", back_populates="leave_modified_by")


    # In User model

    exams_created = relationship("Exam", foreign_keys="[Exam.c_by]", back_populates="exam_created_by")
    exams_modified = relationship("Exam", foreign_keys="[Exam.m_by]", back_populates="exam_modified_by")
    exam_allocations_created = relationship("ExamAllocation", foreign_keys="[ExamAllocation.c_by]", back_populates="allocation_created_by")
    exam_allocations_modified = relationship("ExamAllocation", foreign_keys="[ExamAllocation.m_by]", back_populates="allocation_modified_by")


    subjects_assigned = relationship("SubjectAllocation", foreign_keys="[SubjectAllocation.user_id]", back_populates="assigned_teacher")
    subject_allocations_created = relationship("SubjectAllocation", foreign_keys="[SubjectAllocation.c_by]", back_populates="created_by")
    subject_allocations_modified = relationship("SubjectAllocation", foreign_keys="[SubjectAllocation.m_by]", back_populates="modified_by")

    question_papers_created = relationship("QuestionPaper", foreign_keys="[QuestionPaper.c_by]", back_populates="created_by")
    question_papers_modified = relationship("QuestionPaper", foreign_keys="[QuestionPaper.m_by]", back_populates="modified_by")


    # Inside User model

    marks_created = relationship("Mark", foreign_keys="[Mark.c_by]", back_populates="created_by")
    marks_modified = relationship("Mark", foreign_keys="[Mark.m_by]", back_populates="modified_by")


    timetables_created = relationship("TimeTable", foreign_keys="[TimeTable.c_by]", back_populates="created_by")
    timetables_modified = relationship("TimeTable", foreign_keys="[TimeTable.m_by]", back_populates="modified_by")

    fees_created = relationship("Fees", foreign_keys="[Fees.c_by]", back_populates="created_by")
    fees_modified = relationship("Fees", foreign_keys="[Fees.m_by]", back_populates="modified_by")


    # Inside User model

    fees_history_created = relationship("FeesHistory", foreign_keys="[FeesHistory.c_by]", back_populates="created_by")
    fees_history_modified = relationship("FeesHistory", foreign_keys="[FeesHistory.m_by]", back_populates="modified_by")

    scholarships_created = relationship("Scholarship", foreign_keys="[Scholarship.c_by]", back_populates="created_by")
    scholarships_modified = relationship("Scholarship", foreign_keys="[Scholarship.m_by]", back_populates="modified_by")


    student_scholarships_created = relationship("StudentScholarship", foreign_keys="[StudentScholarship.c_by]", back_populates="created_by")
    student_scholarships_modified = relationship("StudentScholarship", foreign_keys="[StudentScholarship.m_by]", back_populates="modified_by")