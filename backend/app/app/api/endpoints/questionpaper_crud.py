from fastapi import APIRouter, Depends, Form, UploadFile, File, Request
from sqlalchemy.orm import Session
from app.api.deps import get_db, master_access_user, get_user_from_token
from app.models import QuestionPaper, User, ExamAllocation
from datetime import datetime
from utils import file_storage
import os

router = APIRouter()


@router.post("/update-question-paper/{qp_id}")
def update_question_paper(qp_id: int,request: Request,exam_allo_id: int = Form(...),sub_allo_id: int = Form(...),file: UploadFile = File(...),user: User = Depends(master_access_user),db: Session = Depends(get_db),):
    
    question_paper = db.query(QuestionPaper).filter(QuestionPaper.id == qp_id, QuestionPaper.status != -1).first()
    
    if not question_paper:
        return{"Status":0,"Message":"Question Paper not found"}

    if file.content_type != "application/pdf":
        return{"Status":0,"Message":"Only PDF files are allowed"}

    save_full_path, file_relative_path = file_storage(file, file.filename)

    question_paper.name = file.filename
    question_paper.exam_allo_id = exam_allo_id
    question_paper.sub_allo_id = sub_allo_id
    question_paper.qp_link = save_full_path
    question_paper.m_by = user.id
    question_paper.m_at = datetime.now()

    db.commit()
    return {"Status": 1, "Message": "Question Paper updated successfully"}


@router.post("/delete-question-paper/{qp_id}")
def delete_question_paper(qp_id: int, user: User = Depends(master_access_user), db: Session = Depends(get_db)):
    
    question_paper = db.query(QuestionPaper).filter(QuestionPaper.id == qp_id, QuestionPaper.status != -1).first()
    if not question_paper:
        return{"Status":0,"Message":"Question Paper not found"}

    question_paper.status = -1
    question_paper.m_by = user.id
    question_paper.m_at = datetime.now()

    db.commit()
    return {"Status": 1, "Message": "Question Paper deleted successfully"}


@router.post("/view-all-question-papers")
def view_all_question_papers(user: User = Depends(master_access_user), db: Session = Depends(get_db)):
    papers = db.query(QuestionPaper).filter(QuestionPaper.status == 1).all()
    result = []
    for qp in papers:
        result.append({
            "id": qp.id,
            "name": qp.name,
            "exam_allocation_id": qp.exam_allo_id,
            "subject_allocation_id": qp.sub_allo_id,
            "link": qp.qp_link
        })
    return {"Status": 1, "QuestionPapers": result}


@router.post("/student-view-question-papers")
def student_view_question_papers(token: str, db: Session = Depends(get_db)):
    user = get_user_from_token(token, db)
    if isinstance(user, dict):
        return user 

    finished_alloc_ids = db.query(ExamAllocation.id).filter(ExamAllocation.status == 2).all()
    finished_ids = [ea.id for ea in finished_alloc_ids]

    papers = db.query(QuestionPaper).filter(QuestionPaper.status == 1,QuestionPaper.exam_allo_id.in_(finished_ids)).all()

    result = []
    for qp in papers:
        result.append({
            "id": qp.id,
            "name": qp.name,
            "exam_allocation_id": qp.exam_allo_id,
            "subject_allocation_id": qp.sub_allo_id,
            "link": qp.qp_link
        })
    return {"Status": 1, "QuestionPapers": result}
