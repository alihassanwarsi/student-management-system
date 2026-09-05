from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import Student
from app.models import StudentCreate, StudentUpdate

def create_student(db: Session, student: StudentCreate):
    new_student = Student(**student.model_dump())
    db.add(new_student)

    try:
        db.commit()

    except IntegrityError:
        db.rollback()
        raise ValueError("Email already exists")
    
    db.refresh(new_student)
    return new_student

def get_student(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()

def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Student).offset(skip).limit(limit).all()

def update_student(db: Session, student_id: int, data: StudentUpdate):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        return None
    
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(student, key, value)

    try:
        db.commit()

    except IntegrityError:
        db.rollback()
        raise ValueError("Email already exists")
    
    db.refresh(student)
    return student

def delete_student(db: Session, student_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()

    if student:
        db.delete(student)
        db.commit()
        return True
    return False
