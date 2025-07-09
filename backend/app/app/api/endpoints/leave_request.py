from fastapi import APIRouter, Depends, Form, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_user_from_token, teacher_access_user
from app.models import LeaveRequest, User, AcademicYearStudent,AcademicYearClass
from datetime import date

router = APIRouter()

@router.post("/create-leave-request/")
def create_leave_request(token: str = Query(...),from_date: date = Form(...),to_date: date = Form(...),reason: str = Form(...),db: Session = Depends(get_db)):
    
    user = get_user_from_token(token, db)
    
    if isinstance(user, dict) and user.get("Status") == 0:
        return {"Status":0,"Message":"Invalid Token"}

    if user.status != 1:
        return {"Status":0,"Message":"User Inactive"}

    leave = LeaveRequest(
        user_id=user.id,
        from_date=from_date,
        to_date=to_date,
        reason=reason,
        status=1,  
        c_by=user.id,
        m_by=user.id
    )

    db.add(leave)
    db.commit()
    db.refresh(leave)

    return {"status": 1,"message": "Leave request created successfully","leave_id": leave.id}


@router.post("/own-leave-history/")
def view_leave_history(token: str = Query(...),db: Session = Depends(get_db)):
    
    user = get_user_from_token(token, db)

    if isinstance(user, dict) and user.get("Status") == 0:
        return {"Status":0,"Message":"Invalid Token"}

    leaves = db.query(LeaveRequest).filter(LeaveRequest.user_id == user.id).order_by(LeaveRequest.c_at.desc()).all()

    if not leaves:
        return {"status": 0, "message": "No leave history found."}

    leave_list = []
    for leave in leaves:
        leave_list.append({
            "leave_id": leave.id,
            "from_date": leave.from_date,
            "to_date": leave.to_date,
            "reason": leave.reason,
            "status": "Accepted" if leave.status == 1 else "Rejected" if leave.status == 2 else "Pending",
            "created_at": leave.c_at.strftime("%Y-%m-%d %H:%M:%S")
        })

    return {
        "status": 1,
        "user_name": user.name,
        "leave_history": leave_list
    }


@router.post("/view-class-leave-requests/")
def view_class_leave_requests(token: str = Query(...),db: Session = Depends(get_db)):
    
    staff_user = teacher_access_user(token, db)

    if isinstance(staff_user, dict) and staff_user.get("Status") == 0:
        return{"Status":0,"Message":"Unauthorized"}

    staff_classes = db.query(AcademicYearClass).filter(AcademicYearClass.staff_id == staff_user.id,AcademicYearClass.status == 1).all()

    if not staff_classes:
        return {"status": 0, "message": "No class assigned to this staff"}

    class_ids = [c.id for c in staff_classes]

    student_records = db.query(AcademicYearStudent).filter(AcademicYearStudent.ac_class_id.in_(class_ids),AcademicYearStudent.status == 1).all()

    student_ids = [s.student_id for s in student_records]

    if not student_ids:
        return {"status": 0, "message": "No students found in your classes"}

    leave_requests = db.query(LeaveRequest).join(User).filter(LeaveRequest.user_id.in_(student_ids)).order_by(LeaveRequest.c_at.desc()).all()

    if not leave_requests:
        return {"status": 0, "message": "No leave requests submitted by your students"}

    result = []
    for leave in leave_requests:
        result.append({"leave_id": leave.id,"student_name": leave.student.name,"from_date": leave.from_date,"to_date": leave.to_date,
        "reason": leave.reason,"status": "Accepted" if leave.status == 1 else "Rejected" if leave.status == 2 else "Pending",
        "submitted_on": leave.c_at.strftime("%Y-%m-%d %H:%M:%S")})

    return {"status": 1,"message": "Leave requests fetched successfully","leave_requests": result}



@router.post("/update-leave-request/")
def update_leave_request(token: str = Query(...),leave_id: int = Form(...),from_date: str = Form(...),to_date: str = Form(...),reason: str = Form(...),db: Session = Depends(get_db)):
    
    user = get_user_from_token(token, db)
    if isinstance(user, dict) and user.get("Status") == 0:
        return {"Status":0, "Message":"User not found"}

    leave = db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()
    if not leave:
        return{"Status":0, "Message":"Leave request not found"}

    if user.id != leave.user_id and user.user_type != 3:
        return{"Status":0,"Message":"Not authorized to update this leave request"}

    leave.from_date = from_date
    leave.to_date = to_date
    leave.reason = reason
    leave.m_by = user.id
    db.commit()

    return {"status": 1, "message": "Leave request updated successfully"}


@router.post("/delete-leave-request/")
def delete_leave_request(token: str = Query(...),leave_id: int = Query(...),db: Session = Depends(get_db)):
    
    user = get_user_from_token(token, db)
    if isinstance(user, dict) and user.get("Status") == 0:
        return {"Status":0, "Message":"user not found"}

    if user.user_type != 1:
        return{"Status":0, "Message":"Only admin can delete leave requests"}

    leave = db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()
    if not leave:
        return {"Status":0, "Message":"Leave request not found"}

    db.delete(leave)
    db.commit()

    return {"status": 1, "message": "Leave request deleted successfully"}

