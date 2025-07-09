from sqlalchemy import Column, Integer,String,func, ForeignKey, Date, DateTime
from app.db.base_class import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mssql import TINYINT



class AcademicYearClass(Base):
    __tablename__ = 'academic_class'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ac_year_id = Column(Integer, ForeignKey("academic_year.id"))
    standard_id = Column (Integer, ForeignKey("standards.id"))
    section_id = Column (Integer, ForeignKey("section.id"))
    staff_id = Column (Integer, ForeignKey("user.id"))


    status = Column(TINYINT, default=1, comment="1:Active,2:Inactive,-1:Deleted")
    c_by = Column(Integer, ForeignKey('user.id'), comment="Created by User ID")
    c_at = Column(DateTime, default=func.now())
    m_by = Column(Integer, ForeignKey('user.id'), comment="Modified by User ID")
    m_at = Column(DateTime, default=func.now(), onupdate=func.now())


    academic_year = relationship("AcademicYear", back_populates="academic_classes")
    standard = relationship("Standard", back_populates="standard_classes")
    section = relationship("Section", back_populates="section_classes")
    staff = relationship("User", foreign_keys=[staff_id], back_populates="assigned_classes")
    created_by = relationship("User", foreign_keys=[c_by], back_populates="created_academic_classes")
    modified_by = relationship("User", foreign_keys=[m_by], back_populates="modified_academic_classes")
    students = relationship("AcademicYearStudent", back_populates="academic_class")


    exam_allocations = relationship("ExamAllocation", back_populates="allocated_class")


    subject_allocations = relationship("SubjectAllocation", back_populates="academic_class")
