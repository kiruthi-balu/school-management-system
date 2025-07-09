from sqlalchemy import Column, Integer,String,func, ForeignKey, Date, DateTime, Float
from app.db.base_class import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mssql import TINYINT


class StudentScholarship(Base):
    __tablename__ = "student_scholarship"
    id = Column(Integer, primary_key=True, autoincrement=True)
    scholarship_id = Column(Integer, ForeignKey("scholarship.id"))
    acy_stud_id = Column (Integer, ForeignKey("academicyear_student.id"))
    is_paid = Column(String(30), comment="Paid or Pending")

    status = Column(TINYINT, default=1, comment="1:Active,2:Inactive,-1:Deleted")
    c_by = Column(Integer, ForeignKey('user.id'), comment="Created by User ID")
    c_at = Column(DateTime, default=func.now())
    m_by = Column(Integer, ForeignKey('user.id'), comment="Modified by User ID")
    m_at = Column(DateTime, default=func.now(), onupdate=func.now())


    scholarship = relationship("Scholarship", back_populates="student_scholarships")
    academic_year_student = relationship("AcademicYearStudent", back_populates="student_scholarships")

    created_by = relationship("User", foreign_keys=[c_by], back_populates="student_scholarships_created")
    modified_by = relationship("User", foreign_keys=[m_by], back_populates="student_scholarships_modified")
