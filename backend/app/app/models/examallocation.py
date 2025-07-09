from sqlalchemy import Column, Integer,String,func, ForeignKey, Date, DateTime
from app.db.base_class import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mssql import TINYINT



class ExamAllocation(Base):
    __tablename__ = "exam_allocation"
    id = Column(Integer, primary_key=True)
    exam_id = Column (Integer, ForeignKey("exam.id"))
    ac_class_id = Column(Integer, ForeignKey("academic_class.id"))


    status = Column(TINYINT, default=1, comment="1:Active,2:Inactive,-1:Deleted")
    c_by = Column(Integer, ForeignKey('user.id'), comment="Created by User ID")
    c_at = Column(DateTime, default=func.now())
    m_by = Column(Integer, ForeignKey('user.id'), comment="Modified by User ID")
    m_at = Column(DateTime, default=func.now(), onupdate=func.now())


    exam = relationship("Exam", back_populates="allocations")
    allocated_class = relationship("AcademicYearClass", back_populates="exam_allocations")

    allocation_created_by = relationship("User", foreign_keys=[c_by], back_populates="exam_allocations_created")
    allocation_modified_by = relationship("User", foreign_keys=[m_by], back_populates="exam_allocations_modified")

    question_papers = relationship("QuestionPaper", back_populates="exam_allocation")


    marks = relationship("Mark", back_populates="exam_allocation")

   