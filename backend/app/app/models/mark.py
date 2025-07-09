from sqlalchemy import Column, Integer,String,func, ForeignKey, Date, DateTime
from app.db.base_class import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mssql import TINYINT


class Mark(Base):
    __tablename__ = "mark"
    id = Column(Integer, primary_key=True, autoincrement=True)
    acy_stud_id = Column(Integer, ForeignKey('academicyear_student.id'))
    exalloc = Column(Integer, ForeignKey('exam_allocation.id'))
    suballoc = Column(Integer, ForeignKey("subject_allocation.id"))
    obtained_mark = Column(Integer)
    max_mark = Column(Integer)
    status = Column(String(50), comment="Pass or Fail")
    
    c_by = Column(Integer, ForeignKey('user.id'), comment="Created by User ID")
    c_at = Column(DateTime, default=func.now())
    m_by = Column(Integer, ForeignKey('user.id'), comment="Modified by User ID")
    m_at = Column(DateTime, default=func.now(), onupdate=func.now())

    student = relationship("AcademicYearStudent", back_populates="marks")
    exam_allocation = relationship("ExamAllocation", back_populates="marks")
    subject_allocation = relationship("SubjectAllocation", back_populates="marks")

    created_by = relationship("User", foreign_keys=[c_by], back_populates="marks_created")
    modified_by = relationship("User", foreign_keys=[m_by], back_populates="marks_modified")