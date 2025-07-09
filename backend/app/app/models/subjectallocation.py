from sqlalchemy import Column, Integer,String,func, ForeignKey, Date, DateTime
from app.db.base_class import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mssql import TINYINT



class SubjectAllocation(Base):
    __tablename__ = "subject_allocation"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ac_class_id = Column(Integer, ForeignKey("academic_class.id"))
    subject_id = Column (Integer, ForeignKey("subject.id"))
    user_id = Column(Integer,ForeignKey("user.id"))

    status = Column(TINYINT, default=1, comment="1:Active,2:Inactive,-1:Deleted")
    c_by = Column(Integer, ForeignKey('user.id'), comment="Created by User ID")
    c_at = Column(DateTime, default=func.now())
    m_by = Column(Integer, ForeignKey('user.id'), comment="Modified by User ID")
    m_at = Column(DateTime, default=func.now(), onupdate=func.now())


    academic_class = relationship("AcademicYearClass", back_populates="subject_allocations")
    subject = relationship("Subject", back_populates="subject_allocations")
    assigned_teacher = relationship("User", foreign_keys=[user_id], back_populates="subjects_assigned")

    created_by = relationship("User", foreign_keys=[c_by], back_populates="subject_allocations_created")
    modified_by = relationship("User", foreign_keys=[m_by], back_populates="subject_allocations_modified")
   

    question_papers = relationship("QuestionPaper", back_populates="subject_allocation")



    marks = relationship("Mark", back_populates="subject_allocation")


    timetables = relationship("TimeTable", back_populates="subject_allocation")
