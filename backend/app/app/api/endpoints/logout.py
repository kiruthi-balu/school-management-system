from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import *
from app.utils import *
from app.api.deps import  get_db
 


router = APIRouter()

@router.post("/user-logout/")
def user_logout(token:str, db:Session=Depends(get_db)):
    
    db.query(Apitoken).filter(Apitoken.token == token,Apitoken.status == 1).update({
    "status": -1,})
    db.commit()

    return {"Status":1,"Message": "Logout successfully..."}


