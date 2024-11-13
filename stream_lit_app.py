import streamlit as st
import os
import django
from django.conf import settings
from django.core.wsgi import get_wsgi_application

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crud.settings')
django.setup()

from core.models import Students

# Function to trigger page refresh
def refresh_page():
    if 'refresh' not in st.session_state:
        st.session_state['refresh'] = False
    st.session_state['refresh'] = not st.session_state['refresh']

# Streamlit app title and description
st.title("Student Management System")
st.write("A simple CRUD application to manage students.")

# Custom CSS for styling student cards
st.markdown("""
    <style>
        .student-box {
            border: 1px solid #ccc;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 10px;
            background-color: #e6f7ff;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
        }
        .student-header {
            font-weight: bold;
            font-size: 1.1em;
            color: #003366;
            margin-bottom: 5px;
        }
        .student-details {
            color: #333;
        }
        .button-container {
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Display students with edit form directly below each student when editing
st.header("Students List")
students = Students.objects.all()
for stu in students:
    with st.container():
        st.markdown(f"""
            <div class="student-box">
                <div class="student-header">ID: {stu.id} - {stu.name}</div>
                <p class="student-details">Roll: {stu.roll}</p>
                <p class="student-details">City: {stu.city}</p>
                <div class="button-container">
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"Edit {stu.name}", key=f"edit_{stu.id}"):
                st.session_state['edit_id'] = stu.id
        with col2:
            if st.button(f"Delete {stu.name}", key=f"delete_{stu.id}"):
                stu.delete()
                refresh_page()

        st.markdown("</div></div>", unsafe_allow_html=True)
        
        # Inline edit form for the selected student
        if 'edit_id' in st.session_state and st.session_state['edit_id'] == stu.id:
            st.write("### Edit Student")
            with st.form(key=f'edit_student_form_{stu.id}'):
                name = st.text_input("Name", value=stu.name)
                roll = st.text_input("Roll", value=stu.roll)
                city = st.text_input("City", value=stu.city)
                submit_button = st.form_submit_button(label='Update Student')

                if submit_button:
                    stu.name = name
                    stu.roll = roll
                    stu.city = city
                    stu.save()
                    st.success("Student updated successfully!")
                    del st.session_state['edit_id']
                    refresh_page()

# Add new student form
st.header("Add New Student")
with st.form(key='add_student_form'):
    name = st.text_input("Name")
    roll = st.text_input("Roll")
    city = st.text_input("City")
    submit_button = st.form_submit_button(label='Add Student')

    if submit_button:
        new_student = Students(name=name, roll=roll, city=city)
        new_student.save()
        st.success("Student added successfully!")
        refresh_page()
