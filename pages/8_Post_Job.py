import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils.api_client as api

st.title("Post a New Job")

if st.session_state["role"] != 'Recruiter':
    st.warning("Please switch to the Recruiter role to view this page.")
    st.stop()

recruiter_id = st.session_state.get('recruiter_id')
if not recruiter_id:
    st.warning("Please complete your Recruiter Profile first.")
    st.stop()

def get_master_skills():
    try:
        with open('data/skills_master.csv', 'r') as f:
            return [s.strip() for s in f.read().split(',')]
    except:
        return ["Python", "Java", "SQL", "React", "AWS", "Pandas", "Machine Learning"]

master_skills = get_master_skills()

with st.form("post_job_form"):
    title = st.text_input("Job Title")
    description = st.text_area("Job Description")
    job_type = st.selectbox("Job Type", ["Full-time", "Part-time", "Internship", "Contract"])
    min_cgpa = st.slider("Minimum CGPA Required", 0.0, 10.0, 7.0, 0.1)
    
    req_skills = st.multiselect("Required Skills", master_skills)
    
    submitted = st.form_submit_button("Post Job")
    if submitted:
        if title and req_skills:
            data = {
                "recruiter_id": recruiter_id,
                "title": title,
                "description": description,
                "type": job_type,
                "min_cgpa": min_cgpa,
                "required_skills": ", ".join(req_skills)
            }
            with st.spinner("Posting job..."):
                res = api.create_job(data)
                if "error" in res:
                    st.error(res["error"])
                else:
                    st.success(f"Job posted successfully! Job ID: {res.get('job_id')}")
        else:
            st.error("Title and Required Skills are mandatory.")
