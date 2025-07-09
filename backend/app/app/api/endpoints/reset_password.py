from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random
from app.core.security import get_password_hash
from app.models import User, PasswordResetOTP
from app.api.deps import get_db
from app.utils import send_email

router = APIRouter()

@router.post("/request-reset-password/")
async def request_reset_password(email: str = Form(...), db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.email == email, User.status == 1).first()
    if not user:
        return {"Status": 0, "Message": "User not found"}

    otp = f"{random.randint(100000, 999999)}"
    expiry = datetime.now() + timedelta(minutes=2)

    reset_otp = PasswordResetOTP(user_id=user.id, otp=otp, expiry=expiry)
    db.add(reset_otp)
    db.commit()

    result = await send_email(
        to=user.email,
        subject="Password Reset OTP",
        body=f"Hello {user.name},\n\nYour OTP for password reset is: {otp}\nIt will expire in 2 minutes.\n\nRegards,\nLaya School"
    )

    return result



@router.post("/reset-password/")
def reset_password_with_otp(email: str = Form(...),otp: str = Form(...),new_password: str = Form(...),db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == email, User.status == 1).first()
    if not user:
        return {"status": 0, "message": "User not found"}

    otp_entry = (db.query(PasswordResetOTP).filter(PasswordResetOTP.user_id == user.id, PasswordResetOTP.otp == otp).order_by(PasswordResetOTP.id.desc()).first())

    if not otp_entry:
        return {"status": 0, "message": "Invalid OTP"}

    if datetime.now() > otp_entry.expiry:
        return {"status": 0, "message": "OTP has expired"}

    user.password = get_password_hash(new_password)
    db.add(user)
    db.commit()

    return {"status": 1, "message": "Password reset successfully"}