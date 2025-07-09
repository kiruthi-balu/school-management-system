from sqlalchemy import Column, Integer,String,func, ForeignKey, Date, DateTime
from app.db.base_class import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mssql import TINYINT



class Subject(Base):
    __tablename__ = 'subject'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
   
    status = Column(TINYINT, default=1, comment="1:Active,2:Inactive,-1:Deleted")
    c_by = Column(Integer, ForeignKey('user.id'), comment="Created by User ID")
    c_at = Column(DateTime, default=func.now())
    m_by = Column(Integer, ForeignKey('user.id'), comment="Modified by User ID")
    m_at = Column(DateTime, default=func.now(), onupdate=func.now())


    #relation to user table
    create_by = relationship('User', foreign_keys=[c_by], back_populates='created_subjects')
    modify_by = relationship('User', foreign_keys=[m_by], back_populates='modified_subjects')

    subject_allocations = relationship("SubjectAllocation", back_populates="subject")