import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.title("Recruiter Profile")

if st.session_state["role"] != 'Recruiter':
    st.warning("Please switch to the Recruiter role in the sidebar to view this page.")
    st.stop()

with st.form("recruiter_profile_form"):
    st.write("Enter your company and recruiter details.")
    name = st.text_input("Recruiter Name", value="Bob Recruiter")
    company = st.text_input("Company Name", value="Tech Corp")
    email = st.text_input("Work Email", value="bob@techcorp.com")
    
    submitted = st.form_submit_button("Save Profile")
    if submitted:
        if name and company and email:
            # Save to session state
            st.session_state['recruiter_name'] = name
            st.session_state['company'] = company
            st.session_state['recruiter_email'] = email
            
            # Since we have no login and just a seeded database, we'll map to the seeded recruiter ID 1.
            st.session_state['recruiter_id'] = 1
            
            st.success("Recruiter profile saved successfully! You are logged in as Recruiter ID: 1")
        else:
            st.error("All fields are required.")
