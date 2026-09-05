from pydantic import BaseModel, EmailStr

class StudentCreate(BaseModel):
    name: str
    age: int
    department: str
    semester: int
    email: EmailStr

class StudentUpdate(BaseModel):
    name: str 
    age: int 
    department: str 
    semester: int 
    email: EmailStr 

class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    department: str
    semester: int
    email: EmailStr

    class Config:
        from_attributes = True
