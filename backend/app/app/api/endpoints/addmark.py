from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from app.models import Mark, AcademicYearStudent
from app.api.deps import get_db, teacher_access_user
from app.models import User

router = APIRouter()

@router.post("/add-mark/")
def add_mark(acy_stud_id: int = Form(...),exalloc: int = Form(...),suballoc: int = Form(...),obtained_mark: int = Form(...),max_mark: int = Form(...),status: str = Form(...), user: User = Depends(teacher_access_user),db: Session = Depends(get_db)):
    
    
    new_mark = Mark(acy_stud_id=acy_stud_id,
        exalloc=exalloc,
        suballoc=suballoc,
        obtained_mark=obtained_mark,
        max_mark=max_mark,
        status=status, #pass fail status
        c_by=user.id
    )
    
    db.add(new_mark)
    db.commit()
    db.refresh(new_mark)


    return {
        "status": 1,
        "message": "Mark added successfully",
        "mark_id": new_mark.id
    }
