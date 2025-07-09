from sqlalchemy import Column, Integer,String,func, ForeignKey, Date, DateTime
from app.db.base_class import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mssql import TINYINT

class Standard(Base):
    __tablename__ = 'standards'
   
    id = Column(Integer, primary_key=True)
    name = Column(Integer)
    status = Column(TINYINT, default=1, comment="1:Active,2:Inactive,-1:Deleted")
    c_by = Column(Integer, ForeignKey('user.id'), comment="Created by User ID")
    c_at = Column(DateTime, default=func.now())
    m_by = Column(Integer, ForeignKey('user.id'), comment="Modified by User ID")
    m_at = Column(DateTime, default=func.now(), onupdate=func.now())


    cby_standard = relationship('User', foreign_keys=[c_by], back_populates='created_standards')
    mby_standard = relationship('User', foreign_keys=[m_by], back_populates='modified_standards')

    standard_classes = relationship("AcademicYearClass", back_populates="standard")

    fees_records = relationship("Fees", back_populates="standard")