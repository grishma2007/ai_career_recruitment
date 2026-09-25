import streamlit as st
import sys
import os
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils.api_client as api

st.title("Candidate Ranking")

if st.session_state["role"] != 'Recruiter':
    st.warning("Please switch to the Recruiter role to view this page.")
    st.stop()

st.write("Select a job to see candidates ranked by their AI match score.")

# Fetch jobs
jobs_response = api.get_jobs()
if isinstance(jobs_response, dict) and "error" in jobs_response:
    st.error(jobs_response["error"])
    st.stop()

if not jobs_response:
    st.info("No jobs have been posted yet.")
    st.stop()

# Let recruiter pick one of their jobs
# In a real app, we filter by recruiter_id. For simplicity, we just show all jobs.
job_options = {f"ID: {j['job_id']} - {j['title']}": j['job_id'] for j in jobs_response}
selected_job_label = st.selectbox("Select Job Listing", list(job_options.keys()))

if selected_job_label:
    job_id = job_options[selected_job_label]
    
    st.button("Refresh Candidates")
    
    with st.spinner("Fetching applicants..."):
        candidates = api.rank_candidates(job_id)
        
    if isinstance(candidates, dict) and "error" in candidates:
        st.error(candidates["error"])
    elif not candidates:
        st.info("No students have applied to this job yet.")
    else:
        st.success(f"Found {len(candidates)} candidates.")
        
        # Display nicely in a dataframe
        df = pd.DataFrame(candidates)
        df.rename(columns={
            "name": "Candidate Name",
            "email": "Email",
            "cgpa": "CGPA",
            "match_score": "Match Score (%)",
            "status": "Application Status"
        }, inplace=True)
        
        # Format the match score
        df["Match Score (%)"] = df["Match Score (%)"].apply(lambda x: f"{x:.2f}%")
        
        st.dataframe(df, use_container_width=True)
