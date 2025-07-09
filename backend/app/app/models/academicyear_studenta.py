from sqlalchemy import Column, Integer, String, func, ForeignKey, DateTime
from app.db.base_class import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mssql import TINYINT


class AcademicYearStudent(Base):
    __tablename__ = "academicyear_student"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ac_class_id = Column (Integer, ForeignKey("academic_class.id"))
    student_id = Column(Integer, ForeignKey("user.id"))

    status = Column(TINYINT, default=1, comment="1:Active,2:Inactive,-1:Deleted")
    c_by = Column(Integer, ForeignKey('user.id'), comment="Created by User ID")
    c_at = Column(DateTime, default=func.now())
    m_by = Column(Integer, ForeignKey('user.id'), comment="Modified by User ID")
    m_at = Column(DateTime, default=func.now(), onupdate=func.now())


    academic_class = relationship("AcademicYearClass", back_populates="students")
    student = relationship("User", foreign_keys=[student_id], back_populates="enrolled_classes")
    created_by = relationship("User", foreign_keys=[c_by], back_populates="created_academic_students")
    modified_by = relationship("User", foreign_keys=[m_by], back_populates="modified_academic_students")

    marks = relationship("Mark", back_populates="student")


    student_scholarships = relationship("StudentScholarship", back_populates="academic_year_student")