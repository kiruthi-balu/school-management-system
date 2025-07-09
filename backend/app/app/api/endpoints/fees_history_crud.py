from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.models import FeesHistory, Fees, User, AcademicYearStudent, AcademicYearClass
from app.api.deps import get_db, teacher_access_user, get_user_from_token, admin_only_user

router = APIRouter()

@router.post("/feeshistory/create")
def create_fees_history(fees_id: int,paid_school_fees: float,user: User = Depends(teacher_access_user),db: Session = Depends(get_db)):
    
    if user.user_type != 4:
        return{"Status":0,"Message":"Only office staff can create fees history"}

    fees = db.query(Fees).filter(Fees.id == fees_id, Fees.status == 1).first()
    
    if not fees:
        return{"Status":0,"Message":"Fees record not found"}

    balance = fees.school_fees - paid_school_fees

    new_history = FeesHistory(
        fees_id=fees_id,
        paid_school_fees=paid_school_fees,
        bal_school_fees=balance,
        c_by=user.id,
    )
    db.add(new_history)
    db.commit()
    db.refresh(new_history)
    return {"status": 1, "message": "Fees history created successfully", "data": new_history.id}


@router.post("/feeshistory/class/{class_id}")
def view_class_fees_history(class_id: int,user: User = Depends(teacher_access_user),db: Session = Depends(get_db)):
    
    if user.user_type not in [1, 2, 3, 4]:
        return{"Status":0,"Message":"Unauthorized"}

    standard_id = db.query(AcademicYearClass.standard_id).filter(AcademicYearClass.id == class_id).scalar()
    fees_records = (db.query(FeesHistory, User.name.label("student_name")).join(Fees).join(User, FeesHistory.c_by == User.id).filter(Fees.standard_id == standard_id).all())

    results = [
        {
            "fees_history_id": record.FeesHistory.id,
            "student_name": record.student_name,
            "paid": record.FeesHistory.paid_school_fees,
            "balance": record.FeesHistory.bal_school_fees,
        }
        for record in fees_records
    ]

    return {"status": 1, "data": results}


@router.post("/feeshistory/student")
def view_student_fees(token: str = Query(...), db: Session = Depends(get_db)):
    
    user = get_user_from_token(token, db)
    if not isinstance(user, User) or user.user_type != 6:
        return{"Status":0,"Message":"Only students can view their fees"}

    fees_history = db.query(FeesHistory).filter(FeesHistory.c_by == user.id).all()
    
    results = [
        {
            "fees_history_id": record.id,
            "paid": record.paid_school_fees,
            "balance": record.bal_school_fees,
        }
        for record in fees_history
    ]

    return {"status": 1, "data": results}



@router.post("/feeshistory/update/{history_id}")
def update_fees_history(history_id: int,paid_school_fees: float,user: User = Depends(teacher_access_user),db: Session = Depends(get_db)):
    
    if user.user_type != 4:
        return{"Status":0,"Message":"Only office staff can update fees history"}

    history = db.query(FeesHistory).filter(FeesHistory.id == history_id, FeesHistory.status == 1).first()
    
    if not history:
        return{"Status":0,"Message":"Fees history not found"}

    total_fees = history.fees.school_fees
    history.paid_school_fees = paid_school_fees
    history.bal_school_fees = total_fees - paid_school_fees
    history.m_by = user.id
    history.m_at = datetime.now()

    db.commit()
    db.refresh(history)
    return {"status": 1, "message": "Fees history updated successfully"}


@router.post("/feeshistory/delete/{history_id}")
def delete_fees_history(history_id: int,user: User = Depends(teacher_access_user),db: Session = Depends(get_db),):
    
    if user.user_type != 4:
        return{"Status":0,"Message":"Only office staff can delete fees history"}

    history = db.query(FeesHistory).filter(FeesHistory.id == history_id, FeesHistory.status == 1).first()
    
    if not history:
        return{"Status":0,"Message":"Fees history not found"}

    history.status = -1
    history.m_by = user.id
    history.m_at = datetime.now()

    db.commit()
    return {"status": 1, "message": "Fees history deleted successfully"}
