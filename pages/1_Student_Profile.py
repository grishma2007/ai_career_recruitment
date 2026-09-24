import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils.api_client as api

st.title("Student Profile")

if st.session_state["role"] != 'Student':
    st.warning("Please switch to the Student role in the main app to view this page.")
    st.stop()

# Helper to read skills
def get_master_skills():
    try:
        with open('data/skills_master.csv', 'r') as f:
            return [s.strip() for s in f.read().split(',')]
    except:
        return ["Python", "Java", "SQL", "React", "AWS", "Pandas", "Machine Learning"]

master_skills = get_master_skills()

with st.expander("Returning User? Load Profile"):
    load_id = st.number_input("Enter Student ID", min_value=1, step=1)
    if st.button("Load"):
        res = api.get_student(load_id)
        if "error" in res:
            st.error(res["error"])
        else:
            st.session_state['student_id'] = res.get('student_id')
            st.session_state['student_skills'] = res.get('skills', [])
            st.session_state['name'] = res.get('name', '')
            st.session_state['email'] = res.get('email', '')
            st.session_state['branch'] = res.get('branch', 'Computer Science')
            st.session_state['cgpa'] = res.get('cgpa', 8.0)
            st.session_state['attendance'] = res.get('attendance', 80)
            st.session_state['year'] = res.get('year', 1)
            st.session_state['career_goal'] = res.get('career_goal', '')
            st.success("Profile loaded successfully!")
            st.rerun()

if st.session_state.get('student_id'):
    st.info(f"**Currently logged in as Student ID:** {st.session_state['student_id']}")

st.write("### Enter your basic details and current skills")

name = st.text_input("Full Name", value=st.session_state.get('name', ''))
email = st.text_input("Email Address", value=st.session_state.get('email', ''))

branch_options = [
    "Computer Science / Computer Applications",
    "Artificial Intelligence / Machine Learning",
    "Information Technology",
    "Data Science / Data Analytics",
    "Computer Engineering",
    "Electronics / Electronics & Communication",
    "Business Administration / Management",
    "Commerce / Accounting",
    "Marketing / Digital Marketing",
    "Design / Fine Arts / Multimedia",
    "Humanities / Arts",
    "Other"
]
saved_branch = st.session_state.get('branch', 'Computer Science / Computer Applications')

if saved_branch in branch_options:
    branch_index = branch_options.index(saved_branch)
    other_val = ""
else:
    branch_index = branch_options.index("Other")
    other_val = saved_branch
    
selected_branch = st.selectbox("Branch", branch_options, index=branch_index)

if selected_branch == "Other":
    branch = st.text_input("Please specify your branch", value=other_val)
else:
    branch = selected_branch
    
cgpa = st.slider("CGPA", 0.0, 10.0, float(st.session_state.get('cgpa', 8.0)), 0.1)
attendance = st.slider("Attendance %", 0, 100, int(st.session_state.get('attendance', 80)))

saved_year = st.session_state.get('year', 1)
year_options = [1, 2, 3, 4]
year_index = year_options.index(saved_year) if saved_year in year_options else 0
year = st.selectbox("Year of Study", year_options, index=year_index)

career_goal = st.text_input("Career Goal (e.g., Data Scientist)", value=st.session_state.get('career_goal', ''))

saved_skills = st.session_state.get('student_skills', [])
default_multi = [s for s in saved_skills if s in master_skills]
default_custom = [s for s in saved_skills if s not in master_skills]

if default_custom and "Other" not in default_multi:
    default_multi.append("Other")

selected_skills = st.multiselect("Select your skills", master_skills, default=default_multi)

custom_skills = ""
if "Other" in selected_skills:
    custom_skills = st.text_input("Enter your custom skills (comma-separated)", value=", ".join(default_custom))

submitted = st.button("Save Profile")
if submitted:
    if name and email:
        # Combine standard skills with custom skills
        final_skills = [s for s in selected_skills if s != "Other"]
        if custom_skills:
            final_skills.extend([s.strip() for s in custom_skills.split(",") if s.strip()])
            
        # Save to session
        st.session_state['name'] = name
        st.session_state['email'] = email
        st.session_state['branch'] = branch
        st.session_state['year'] = year
        st.session_state['attendance'] = attendance
        st.session_state['career_goal'] = career_goal
        st.session_state['student_skills'] = final_skills
        st.session_state['cgpa'] = cgpa
        
        # Save to backend
        data = {
            "name": name, "email": email, "branch": branch, 
            "cgpa": cgpa, "attendance": attendance, 
            "year": year, "career_goal": career_goal,
            "skills": final_skills
        }
        res = api.create_student(data)
        if "error" in res:
            st.error(res["error"])
        else:
            st.session_state['student_id'] = res.get('student_id')
            st.success(f"Profile saved! Student ID: {res.get('student_id')}")
    else:
        st.error("Name and Email are required.")

if st.session_state.get('student_id'):
    st.write("---")
    st.write("### Delete Profile")
    st.warning("Warning: This action is permanent and will delete your profile and all applications.")
    if st.button("Delete My Profile", type="primary"):
        res = api.delete_student(st.session_state['student_id'])
        if "error" in res:
            st.error(res["error"])
        else:
            st.success("Profile deleted.")
            for key in list(st.session_state.keys()):
                if key != 'role':
                    del st.session_state[key]
            import time
            time.sleep(1)
            st.rerun()
