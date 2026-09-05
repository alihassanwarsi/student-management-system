import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

# --------------------------------------------------
# Page setup
# --------------------------------------------------

st.set_page_config(
    page_title="Student Management System",
    page_icon="🎓",
    layout="centered",
)

# --------------------------------------------------
# Clean Styling
# --------------------------------------------------

st.markdown(
    """
    <style>
        /* Widen the main hero section/container comfortably */
        [data-testid="stMainBlockContainer"] {
            max-width: 950px;
            padding-top: 2rem;
        }

        /* Make sidebar navigation text larger */
        [data-testid="stSidebar"] .stRadio p {
            font-size: 1.15rem !important;
            padding-bottom: 0.2rem;
        }

        /* Keep the custom student card for the search results layout */
        .student-card {
            border: 1px solid rgba(128, 128, 128, 0.2);
            border-radius: 8px;
            padding: 1.5rem;
            margin-top: 1rem;
        }

        .student-row {
            display: flex;
            justify-content: space-between;
            padding: 0.5rem 0;
            border-bottom: 1px solid rgba(128, 128, 128, 0.1);
        }

        .student-row:last-child {
            border-bottom: none;
        }

        .student-label {
            color: rgba(128, 128, 128, 0.9);
        }

        .student-value {
            font-weight: 600;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# API helper
# --------------------------------------------------

def api_request(method, endpoint, **kwargs):
    try:
        return requests.request(
            method,
            f"{API_URL}{endpoint}",
            timeout=5,
            **kwargs,
        )

    except requests.exceptions.ConnectionError:
        st.error("FastAPI server is not running.")
        return None

    except requests.exceptions.Timeout:
        st.error("The request timed out.")
        return None

    except requests.exceptions.RequestException:
        st.error("Could not connect to the API.")
        return None


def get_error_detail(response, fallback):
    try:
        return response.json().get("detail", fallback)
    except ValueError:
        return fallback

# --------------------------------------------------
# Fetch students
# --------------------------------------------------

def fetch_students():
    response = api_request("GET", "/students/")

    if response and response.status_code == 200:
        return response.json()

    return None

# --------------------------------------------------
# Reusable student card
# --------------------------------------------------

def render_student_card(student):
    st.markdown(
        """
        <div class="student-card">
            <div class="student-row">
                <span class="student-label">ID</span>
                <span class="student-value">{id}</span>
            </div>
            <div class="student-row">
                <span class="student-label">Name</span>
                <span class="student-value">{name}</span>
            </div>
            <div class="student-row">
                <span class="student-label">Age</span>
                <span class="student-value">{age}</span>
            </div>
            <div class="student-row">
                <span class="student-label">Department</span>
                <span class="student-value">{department}</span>
            </div>
            <div class="student-row">
                <span class="student-label">Semester</span>
                <span class="student-value">{semester}</span>
            </div>
            <div class="student-row">
                <span class="student-label">Email</span>
                <span class="student-value">{email}</span>
            </div>
        </div>
        """.format(
            id=student["id"],
            name=student["name"],
            age=student["age"],
            department=student["department"],
            semester=student["semester"],
            email=student["email"],
        ),
        unsafe_allow_html=True,
    )

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:
    st.markdown("# Student Management System")
    st.write("---")

    page = st.radio(
        "Navigation",
        [
            "View All Students",
            "Add Student",
            "Search Student",
            "Update Student",
            "Delete Student",
        ],
        label_visibility="collapsed",
    )

# --------------------------------------------------
# View All Students
# --------------------------------------------------

if page == "View All Students":
    st.title("View All Students")

    students = fetch_students()

    if students is not None:
        if students:
            columns = ["id", "name", "age", "department", "semester", "email"]
            st.dataframe(
                [{col: s[col] for col in columns} for s in students],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No students found.")

# --------------------------------------------------
# Add Student
# --------------------------------------------------

elif page == "Add Student":
    st.title("Add Student")

    with st.form("add_student_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Name")

            age = st.number_input(
                "Age",
                min_value=1,
                max_value=100,
                value=18,
                step=1,
            )

            department = st.text_input("Department")

        with col2:
            semester = st.number_input(
                "Semester",
                min_value=1,
                max_value=8,
                value=1,
                step=1,
            )

            email = st.text_input("Email")

        submitted = st.form_submit_button(
            "Add Student",
            use_container_width=True,
        )

    if submitted:
        if not name.strip() or not department.strip() or not email.strip():
            st.warning("Please complete all fields.")
        else:
            payload = {
                "name": name.strip(),
                "age": int(age),
                "department": department.strip(),
                "semester": int(semester),
                "email": email.strip(),
            }

            response = api_request("POST", "/students/", json=payload)

            if response and response.status_code == 200:
                st.success("Student added successfully.")
            elif response:
                st.error(get_error_detail(response, "Failed to add student."))

# --------------------------------------------------
# Search Student
# --------------------------------------------------

elif page == "Search Student":
    st.title("Search Student")

    with st.form("search_student_form"):
        student_id = st.number_input(
            "Student ID",
            min_value=1,
            step=1,
            value=1,
        )

        submitted = st.form_submit_button(
            "Search",
            use_container_width=True,
        )

    if submitted:
        response = api_request("GET", f"/students/{int(student_id)}")

        if response and response.status_code == 200:
            render_student_card(response.json())
        elif response and response.status_code == 404:
            st.warning("Student not found.")
        elif response:
            st.error("Failed to search for student.")

# --------------------------------------------------
# Update Student
# --------------------------------------------------

elif page == "Update Student":
    st.title("Update Student")

    with st.form("load_student_form"):
        student_id = st.number_input(
            "Student ID",
            min_value=1,
            step=1,
            value=1,
        )

        load_clicked = st.form_submit_button(
            "Load Student",
            use_container_width=True,
        )

    if load_clicked:
        response = api_request("GET", f"/students/{int(student_id)}")

        if response and response.status_code == 200:
            st.session_state["student_to_update"] = response.json()
        elif response and response.status_code == 404:
            st.session_state.pop("student_to_update", None)
            st.warning("Student not found.")
        elif response:
            st.error("Failed to load student.")

    student = st.session_state.get("student_to_update")

    if student:
        with st.form("update_student_form"):
            col1, col2 = st.columns(2)

            with col1:
                name = st.text_input("Name", value=student["name"])

                age = st.number_input(
                    "Age",
                    min_value=1,
                    max_value=100,
                    value=student["age"],
                    step=1,
                )

                department = st.text_input("Department", value=student["department"])

            with col2:
                semester = st.number_input(
                    "Semester",
                    min_value=1,
                    max_value=8,
                    value=student["semester"],
                    step=1,
                )

                email = st.text_input("Email", value=student["email"])

            submitted = st.form_submit_button(
                "Save Changes",
                use_container_width=True,
            )

        if submitted:
            payload = {
                "name": name.strip(),
                "age": int(age),
                "department": department.strip(),
                "semester": int(semester),
                "email": email.strip(),
            }

            response = api_request(
                "PUT",
                f"/students/{student['id']}",
                json=payload,
            )

            if response and response.status_code == 200:
                st.success("Student updated successfully.")
                st.session_state.pop("student_to_update", None)
            elif response:
                st.error(get_error_detail(response, "Failed to update student."))

# --------------------------------------------------
# Delete Student
# --------------------------------------------------

elif page == "Delete Student":
    st.title("Delete Student")

    with st.form("delete_student_form"):
        student_id = st.number_input(
            "Student ID",
            min_value=1,
            step=1,
            value=1,
        )

        confirm = st.checkbox("I confirm I want to delete this student.")

        submitted = st.form_submit_button(
            "Delete Student",
            use_container_width=True,
        )

    if submitted:
        if not confirm:
            st.warning("Please check the confirmation box before deleting.")
        else:
            response = api_request("DELETE", f"/students/{int(student_id)}")

            if response and response.status_code == 200:
                st.success("Student deleted successfully.")
            elif response and response.status_code == 404:
                st.warning("Student not found.")
            elif response:
                st.error("Failed to delete student.")