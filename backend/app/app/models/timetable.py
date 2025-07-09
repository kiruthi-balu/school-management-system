from sqlalchemy import Column, Integer,String,func, ForeignKey, Date, DateTime
from app.db.base_class import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mssql import TINYINT


class TimeTable(Base):
    __tablename__ = "timetable"
    id = Column(Integer, primary_key=True, autoincrement=True)
    sub_allo_id = Column(Integer, ForeignKey("subject_allocation.id"))
    day = Column(String(20))
    period = Column (Integer)


    status = Column(TINYINT, default=1, comment="1:Active,2:Inactive,-1:Deleted")
    c_by = Column(Integer, ForeignKey('user.id'), comment="Created by User ID")
    c_at = Column(DateTime, default=func.now())
    m_by = Column(Integer, ForeignKey('user.id'), comment="Modified by User ID")
    m_at = Column(DateTime, default=func.now(), onupdate=func.now())


    subject_allocation = relationship("SubjectAllocation", back_populates="timetables")

    created_by = relationship("User", foreign_keys=[c_by], back_populates="timetables_created")
    modified_by = relationship("User", foreign_keys=[m_by], back_populates="timetables_modified")