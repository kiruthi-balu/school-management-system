from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import User, Apitoken
from app.api.deps import get_db, get_user_from_token

router = APIRouter()

@router.post("/delete-user/{user_id}")
def delete_user(user_id: int,token: str,db: Session = Depends(get_db)):
    
    current_user = get_user_from_token(token, db)

    if current_user.user_type != 1:
        return {"Status": 0 , "Message":"Only admins can delete users"}

    if current_user.id == user_id:
       return {"Status":0 , "Message":"You can't delete your own account"}
    
    user_to_delete = db.query(User).filter(User.id == user_id, User.status == 1).first()
    if not user_to_delete:
        return {"Status": 0 , "Message":"User not found or already deleted"}

    user_to_delete.status = -1
    db.commit()

    return {"status": 1, "message": f"User ID {user_id} deleted successfully"}
