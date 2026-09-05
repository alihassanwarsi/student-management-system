# Student Management System

A simple REST API and Streamlit interface for managing student records.

## Tech Stack

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* Streamlit

## Features

* Add a student
* View all students
* Search for a student by ID
* Update student information
* Delete a student
* Email validation
* Duplicate email handling
* API documentation with Swagger UI

## Project Structure

```text
student-management-system/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── crud.py
├── ui.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Run the API

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## Run the Streamlit UI

In a separate terminal:

```bash
streamlit run ui.py
```

## API Endpoints

| Method | Route                    | Description       |
| ------ | ------------------------ | ----------------- |
| GET    | `/`                      | Check API status  |
| POST   | `/students/`             | Add a student     |
| GET    | `/students/`             | View all students |
| GET    | `/students/{student_id}` | Get a student     |
| PUT    | `/students/{student_id}` | Update a student  |
| DELETE | `/students/{student_id}` | Delete a student  |

## API Documentation

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## Example Request

Create a student using `POST /students/`:

```json
{
  "name": "Ali Hassan",
  "age": 21,
  "department": "Artificial Intelligence",
  "semester": 5,
  "email": "ali123@gmail.com"
}
```
