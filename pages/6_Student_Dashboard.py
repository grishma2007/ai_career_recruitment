import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils.api_client as api
import pandas as pd

st.title("Student Dashboard")

if st.session_state["role"] != 'Student':
    st.warning("Please switch to the Student role to view this page.")
    st.stop()

skills = st.session_state.get('student_skills', [])
cgpa = st.session_state.get('cgpa', 0.0)
student_id = st.session_state.get('student_id')

col1, col2, col3 = st.columns(3)
col1.metric("Skills Registered", len(skills))
col2.metric("Current CGPA", cgpa)
col3.metric("Student ID", student_id if student_id else "Not Saved")

st.header("Job Matches")

if not skills:
    st.info("Update your profile to see job matches.")
else:
    if "matches" not in st.session_state:
        st.session_state["matches"] = []

    if st.button("Refresh Matches") or not st.session_state["matches"]:
        with st.spinner("Finding the best jobs for you..."):
            res = api.match_jobs(skills, cgpa)
            if "error" in res:
                st.error(res["error"])
            else:
                st.session_state["matches"] = res.get("matches", [])

    matches = st.session_state["matches"]
    if not matches:
        st.info("No matching jobs found.")
    else:
        for m in matches:
            with st.expander(f"{m['title']} (Match: {m['match_score']}%)"):
                st.write(f"**Required Skills:** {m['required_skills']}")
                if student_id:
                    if st.button("Apply", key=f"apply_{m['job_id']}"):
                        apply_res = api.apply_job(student_id, m['job_id'], m['match_score'])
                        if "error" in apply_res:
                            st.error(apply_res["error"])
                        else:
                            st.success("Successfully applied!")
                else:
                    st.warning("Save your profile to apply.")
