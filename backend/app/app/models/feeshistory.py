from sqlalchemy import Column, Integer,String,func, ForeignKey, Date, DateTime, Float
from app.db.base_class import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mssql import TINYINT



class FeesHistory(Base):
    __tablename__ = 'feeshistory'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fees_id = Column(Integer, ForeignKey("fees.id"))
    paid_school_fees = Column(Float)
    bal_school_fees = Column(Float)

    status = Column(TINYINT, default=1, comment="1:Active,2:Inactive,-1:Deleted")
    c_by = Column(Integer, ForeignKey('user.id'), comment="Created by User ID")
    c_at = Column(DateTime, default=func.now())
    m_by = Column(Integer, ForeignKey('user.id'), comment="Modified by User ID")
    m_at = Column(DateTime, default=func.now(), onupdate=func.now())

    fees = relationship("Fees", back_populates="fees_history")

    created_by = relationship("User", foreign_keys=[c_by], back_populates="fees_history_created")
    modified_by = relationship("User", foreign_keys=[m_by], back_populates="fees_history_modified")

   