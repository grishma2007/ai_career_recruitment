import streamlit as st
import sys
import os
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils.api_client as api

st.title("Recruiter Dashboard")

if st.session_state["role"] != 'Recruiter':
    st.warning("Please switch to the Recruiter role to view this page.")
    st.stop()

st.header("Overview")

jobs_response = api.get_jobs()
if isinstance(jobs_response, dict) and "error" in jobs_response:
    st.error("Error loading jobs.")
    jobs = []
else:
    jobs = jobs_response

col1, col2 = st.columns(2)
col1.metric("Total Active Jobs", len(jobs))

st.header("Manage Candidates")

if jobs:
    for j in jobs:
        with st.expander(f"Job: {j['title']} (ID: {j['job_id']})"):
            j_col1, j_col2 = st.columns([4, 1])
            j_col1.write(f"**Skills Required:** {j['required_skills']}")
            if j_col2.button("Delete Job", key=f"delete_job_{j['job_id']}"):
                res = api.delete_job(j['job_id'])
                if "error" in res:
                    st.error(res["error"])
                else:
                    st.success("Job deleted!")
                    st.rerun()

            candidates = api.rank_candidates(j['job_id'])
            if not candidates or (isinstance(candidates, dict) and "error" in candidates):
                st.write("No applicants yet.")
            else:
                for idx, c in enumerate(candidates):
                    # Use a unique key for each button
                    c_col1, c_col2, c_col3 = st.columns([2, 1, 1])
                    c_col1.write(f"**{c['name']}** - Match: {c['match_score']}% - CGPA: {c['cgpa']}")
                    
                    # Dummy state management for buttons
                    key = f"status_{j['job_id']}_{c['email']}_{idx}"
                    if key not in st.session_state:
                        st.session_state[key] = c['status']
                    
                    current_status = st.session_state[key]
                    
                    if current_status == "Applied":
                        if c_col2.button("Shortlist", key=f"shortlist_{key}"):
                            st.session_state[key] = "Shortlisted"
                            st.rerun()
                        if c_col3.button("Reject", key=f"reject_{key}"):
                            st.session_state[key] = "Rejected"
                            st.rerun()
                    else:
                        c_col2.write(f"*Status: {current_status}*")
else:
    st.info("No jobs posted. Use the Post Job page to get started.")
