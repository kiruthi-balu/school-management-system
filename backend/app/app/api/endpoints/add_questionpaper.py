from fastapi import APIRouter, Depends, Form, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, master_access_user
from app.models import QuestionPaper, User
from datetime import datetime
from utils import file_storage
from fastapi.requests import Request  


router = APIRouter()

@router.post("/add-question-paper")
def add_question_paper(request:Request,exam_allo_id: int = Form(...),sub_allo_id: int = Form(...),file: UploadFile = File(...),user: User = Depends(master_access_user),db: Session = Depends(get_db)):
    
    if file.content_type != "application/pdf":
        return {"Status":0,"Message":"Only PDF files are allowed"}

    save_full_path, file_relative_path = file_storage(file, file.filename)
    file_url = save_full_path
    print(file_url)

    question_paper = QuestionPaper(
        name=file.filename,
        exam_allo_id=exam_allo_id,
        sub_allo_id=sub_allo_id,
        qp_link=file_url,
        c_by=user.id)
    
    db.add(question_paper)
    db.commit()
    
    download_link = f"download-question-paper/{file_url}"

    return {"Status": 1 , "Message": "Question Paper added successfully","id":question_paper.id,"Download Question paper":download_link}