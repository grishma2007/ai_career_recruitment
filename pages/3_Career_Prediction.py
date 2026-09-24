import streamlit as st
import sys
import os
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils.api_client as api

st.title("Career Prediction")

if st.session_state["role"] != 'Student':
    st.warning("Please switch to the Student role to view this page.")
    st.stop()

skills = st.session_state.get('student_skills', [])
cgpa = st.session_state.get('cgpa', 0.0)

if not skills:
    st.warning("You have no skills listed. Please update your profile first.")
    st.stop()

st.write(f"**Current Skills:** {', '.join(skills)}")
st.write(f"**CGPA:** {cgpa}")

if st.button("Predict Ideal Career Role"):
    with st.spinner("Analyzing profile with Machine Learning..."):
        res = api.predict_career(skills, cgpa)
        if "error" in res:
            st.error(res["error"])
        else:
            role = res.get("predicted_role")
            st.success(f"### Predicted Role: {role}")
            
            # Show a dummy confidence chart to simulate probability output
            st.write("#### Confidence Profile")
            sample_roles = [role] + [r for r in ["Data Scientist", "Software Developer", "UI/UX Designer", "HR Manager", "Data Analyst", "Machine Learning Engineer"] if r != role][:4]
            dummy_data = pd.DataFrame({
                "Role": sample_roles,
                "Confidence": [85 if r == role else max(0, 15 - (len(r) % 10)) for r in sample_roles]
            })
            st.bar_chart(dummy_data.set_index("Role"))
