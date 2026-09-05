from sqladmin import Admin, ModelView
from app.database import Student, engine
from app.main import app

admin = Admin(app, engine)

class StudentAdmin(ModelView, model=Student):
    column_list = [
        Student.id,
        Student.name,
        Student.age,
        Student.department,
        Student.semester,
        Student.email
    ]

admin.add_view(StudentAdmin)
