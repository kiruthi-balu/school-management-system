from fastapi import APIRouter, Depends, Form, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, admin_only_user, get_user_from_token
from app.models import Fees, Standard

router = APIRouter()


@router.post("/create-fees/")
def create_fees(standard_id: int = Form(...),school_fees: float = Form(...),admin_user = Depends(admin_only_user),db: Session = Depends(get_db)):
    
    fees_record = Fees(standard_id=standard_id,school_fees=school_fees,c_by=admin_user.id)
    
    db.add(fees_record)
    db.commit()
    db.refresh(fees_record)

    return {
        "status": 1,
        "message": "Fees record created successfully",
        "data": {"id": fees_record.id}
    }


@router.post("/update-fees/")
def update_fees(fees_id: int = Form(...),school_fees: float = Form(...),admin_user = Depends(admin_only_user),db: Session = Depends(get_db)):
    
    fees_record = db.query(Fees).filter(Fees.id == fees_id, Fees.status != -1).first()
    if not fees_record:
        return{"Status":0,"Message":"Fees record not found"}

    fees_record.school_fees = school_fees
    fees_record.m_by = admin_user.id
    db.commit()

    return {"status": 1, "message": "Fees record updated successfully"}


@router.post("/delete-fees/")
def delete_fees(fees_id: int = Query(...),admin_user = Depends(admin_only_user),db: Session = Depends(get_db)):
    
    fees_record = db.query(Fees).filter(Fees.id == fees_id, Fees.status != -1).first()
    if not fees_record:
        return{"Status":0,"Message":"Fees record not found"}

    fees_record.status = -1
    fees_record.m_by = admin_user.id
    db.commit()

    return {"status": 1, "message": "Fees record deleted successfully"}


@router.post("/view-fees/")
def view_fees(token: str = Query(...), db: Session = Depends(get_db)):
    
    user = get_user_from_token(token, db)
    if isinstance(user, dict) and user.get("Status") == 0:
        return user

    fees_list = (db.query(Fees.id,Standard.name.label("standard_name"),Fees.school_fees)
        .join(Standard, Fees.standard_id == Standard.standard_id).filter(Fees.status == 1).order_by(Standard.name).all())

    return {"status": 1, "data": fees_list}
