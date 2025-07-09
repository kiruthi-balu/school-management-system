from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import Scholarship, User
from app.api.deps import get_db, master_access_user
from datetime import datetime
from typing import Optional

router = APIRouter()

@router.post("/create-scholarship")
def create_scholarship(name: str,amount: float,user: User = Depends(master_access_user),db: Session = Depends(get_db)):
    
    scholarship = Scholarship(name=name, amount=amount, c_by=user.id)
    db.add(scholarship)
    db.commit()
    db.refresh(scholarship)
    return {"status": 1, "message": "Scholarship created", "id": scholarship.id}


@router.post("/view-scholarships")
def view_scholarships(user: User = Depends(master_access_user),db: Session = Depends(get_db)):
    
    scholarships = db.query(Scholarship).filter(Scholarship.status != -1).all()
    return {"status": 1, "scholarships": [
        {
            "id": s.id,
            "name": s.name,
            "amount": s.amount,
            "status": s.status
        } for s in scholarships
    ]}

@router.post("/update-scholarship/{scholarship_id}")
def update_scholarship(scholarship_id: int,name: Optional[str] = None,amount: Optional[float] = None,user: User = Depends(master_access_user),db: Session = Depends(get_db)):
    
    scholarship = db.query(Scholarship).filter(Scholarship.id == scholarship_id, Scholarship.status != -1).first()
    
    if not scholarship:
        return{"Status":0,"Message":"Scholarship not found"}
    
    if name:
        scholarship.name = name
    if amount is not None:
        scholarship.amount = amount
    scholarship.m_by = user.id
    scholarship.m_at = datetime.now()

    db.commit()
    return {"status": 1, "message": "Scholarship updated successfully"}

@router.post("/delete-scholarship/{scholarship_id}")
def delete_scholarship(scholarship_id: int,user: User = Depends(master_access_user),db: Session = Depends(get_db)):
    
    scholarship = db.query(Scholarship).filter(Scholarship.id == scholarship_id, Scholarship.status != -1).first()
    if not scholarship:
        return{"Status":0,"Message":"Scholarship not found"}

    scholarship.status = -1
    scholarship.m_by = user.id
    scholarship.m_at = datetime.now()
    db.commit()
    return {"status": 1, "message": "Scholarship deleted successfully"}
