import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("Student Management System")

response = requests.get(f"{API_URL}/")

if response.status_code == 200:
    st.success(response.json()["message"])
else:
    st.error("API is not running.")