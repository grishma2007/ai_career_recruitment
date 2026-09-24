import streamlit as st
import os

# Initialize session state globally
if 'role' not in st.session_state:
    st.session_state['role'] = 'Student'
if 'student_id' not in st.session_state:
    st.session_state['student_id'] = None
if 'recruiter_id' not in st.session_state:
    st.session_state['recruiter_id'] = None
if 'student_skills' not in st.session_state:
    st.session_state['student_skills'] = []
if 'cgpa' not in st.session_state:
    st.session_state['cgpa'] = 0.0

st.sidebar.title("Platform Settings")
selected_role = st.sidebar.radio("Select your role:", ("Student", "Recruiter"), index=0 if st.session_state['role'] == 'Student' else 1)

if selected_role != st.session_state['role']:
    st.session_state['role'] = selected_role
    st.rerun()

# Define pages
student_profile = st.Page("pages/1_Student_Profile.py", title="Profile", icon="👤")
career_prediction = st.Page("pages/3_Career_Prediction.py", title="Career Prediction", icon="🎯")
academic_risk = st.Page("pages/4_Academic_Risk.py", title="Academic Risk", icon="⚠️")
recommendations = st.Page("pages/5_Recommendations.py", title="Recommendations", icon="💡")
student_dashboard = st.Page("pages/6_Student_Dashboard.py", title="Dashboard", icon="📊")

recruiter_profile = st.Page("pages/7_Recruiter_Profile.py", title="Company Profile", icon="🏢")
post_job = st.Page("pages/8_Post_Job.py", title="Post Job", icon="📝")
candidate_ranking = st.Page("pages/9_Candidate_Ranking.py", title="Candidate Ranking", icon="🏆")
recruiter_dashboard = st.Page("pages/10_Recruiter_Dashboard.py", title="Dashboard", icon="📈")

if st.session_state['role'] == 'Student':
    pg = st.navigation([student_profile, career_prediction, academic_risk, recommendations, student_dashboard])
else:
    pg = st.navigation([recruiter_profile, post_job, candidate_ranking, recruiter_dashboard])

pg.run()
