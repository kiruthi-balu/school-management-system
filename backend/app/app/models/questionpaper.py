from sqlalchemy import Column, Integer,String,func, ForeignKey, Date, DateTime
from app.db.base_class import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mssql import TINYINT



class QuestionPaper(Base):
    __tablename__ = 'questionpaper'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    exam_allo_id = Column(Integer, ForeignKey("exam_allocation.id"))
    sub_allo_id = Column(Integer,ForeignKey("subject_allocation.id"))
    qp_link = Column(String(100))


    status = Column(TINYINT, default=1, comment="1:Active,2:Inactive,-1:Deleted")
    c_by = Column(Integer, ForeignKey('user.id'), comment="Created by User ID")
    c_at = Column(DateTime, default=func.now())
    m_by = Column(Integer, ForeignKey('user.id'), comment="Modified by User ID")
    m_at = Column(DateTime, default=func.now(), onupdate=func.now())


    exam_allocation = relationship("ExamAllocation", back_populates="question_papers")
    subject_allocation = relationship("SubjectAllocation", back_populates="question_papers")

    created_by = relationship("User", foreign_keys=[c_by], back_populates="question_papers_created")
    modified_by = relationship("User", foreign_keys=[m_by], back_populates="question_papers_modified")

