from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.models import StudentCreate,StudentUpdate, StudentResponse
from app.database import get_db
from app.crud import create_student, get_student, get_students, update_student, delete_student

app = FastAPI()

@app.get("/")
def health_check():
    return {"message": "API running successfully!"}

@app.post("/students/", response_model=StudentResponse)
def create_new_student(student: StudentCreate, db: Session = Depends(get_db)):
    try:
        return create_student(db, student)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/students/", response_model=list[StudentResponse])
def read_students(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=100), db: Session = Depends(get_db)):
    return get_students(db, skip, limit)

@app.get("/students/{student_id}", response_model=StudentResponse)
def read_student(student_id: int, db: Session = Depends(get_db)):
    student = get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student_data(student_id: int, student_data: StudentUpdate, db: Session = Depends(get_db)): 
    try:
        updated = update_student(db, student_id, student_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not updated:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated

@app.delete("/students/{student_id}")
def delete_student_data(student_id: int, db: Session = Depends(get_db)):
    result = delete_student(db, student_id)
    if not result:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}