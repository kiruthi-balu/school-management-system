from sqlalchemy import Column, Integer, String,Date, func, ForeignKey, DateTime
from app.db.base_class import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mssql import TINYINT


class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    date = Column(Date)

    present = Column(String(20)) #present or abscent
    status =  Column (TINYINT, default="1", comment="1:Fullday, 2:Morning, 3:Afternoon, 4:On Duty")

    c_by = Column(Integer, ForeignKey('user.id'), comment="Created by User ID")
    c_at = Column(DateTime, default=func.now())
    m_by = Column(Integer, ForeignKey('user.id'), comment="Modified by User ID")
    m_at = Column(DateTime, default=func.now(), onupdate=func.now())


    student = relationship("User", foreign_keys=[user_id], back_populates="student_attendance")
    attendance_creator = relationship("User", foreign_keys=[c_by], back_populates="created_attendance_entries")
    attendance_modifier = relationship("User", foreign_keys=[m_by], back_populates="modified_attendance_entries")
