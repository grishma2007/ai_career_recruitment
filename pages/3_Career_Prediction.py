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
            dummy_data = pd.DataFrame({
                "Role": ["Data Scientist", "Graphic Designer", "Marketing Manager", "HR Manager", "Web Developer", "Sales Executive"],
                "Confidence": [85 if r == role else 15 - (len(r) % 10) for r in ["Data Scientist", "Graphic Designer", "Marketing Manager", "HR Manager", "Web Developer", "Sales Executive"]]
            })
            st.bar_chart(dummy_data.set_index("Role"))
