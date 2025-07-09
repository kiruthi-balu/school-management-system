from sqlalchemy import Column, Integer,String,func, ForeignKey, Date, DateTime
from app.db.base_class import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mssql import TINYINT




class LeaveRequest(Base):
    __tablename__= "leaverequest"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    from_date = Column(Date)
    to_date = Column(Date)
    reason = Column(String(255))
    status = Column(TINYINT, default=1, comment="1:Accept, 2:Reject")

    c_by = Column(Integer, ForeignKey('user.id'), comment="Created by User ID")
    c_at = Column(DateTime, default=func.now())
    m_by = Column(Integer, ForeignKey('user.id'), comment="Modified by User ID")
    m_at = Column(DateTime, default=func.now(), onupdate=func.now())


    student = relationship("User", foreign_keys=[user_id], back_populates="leave_requests")
    leave_created_by = relationship("User", foreign_keys=[c_by], back_populates="leave_requests_created")
    leave_modified_by = relationship("User", foreign_keys=[m_by], back_populates="leave_requests_modified")

  