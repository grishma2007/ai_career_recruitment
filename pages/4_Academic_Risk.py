import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils.api_client as api

st.title("Academic Risk Predictor")

if st.session_state["role"] != 'Student':
    st.warning("Please switch to the Student role to view this page.")
    st.stop()

st.write("Evaluate your current academic trajectory.")

with st.form("risk_form"):
    attendance = st.slider("Attendance %", 0, 100, 75)
    internal_marks = st.slider("Internal Marks %", 0, 100, 60)
    study_hours = st.slider("Weekly Self-Study Hours", 0, 40, 10)
    backlogs = st.number_input("Current Backlogs", 0, 10, 0)
    cgpa = st.session_state.get('cgpa', 7.0)
    st.write(f"Using CGPA from profile: {cgpa}")
    
    submitted = st.form_submit_button("Predict Risk")
    if submitted:
        data = {
            "attendance": attendance,
            "internal_marks": internal_marks,
            "study_hours": study_hours,
            "backlogs": backlogs,
            "cgpa": cgpa
        }
        with st.spinner("Analyzing metrics..."):
            res = api.predict_risk(data)
            if "error" in res:
                st.error(res["error"])
            else:
                risk = res.get("risk_level")
                if risk == "Low":
                    st.success("### Risk Level: LOW")
                    st.write("You are on track! Keep up the good work.")
                elif risk == "Medium":
                    st.warning("### Risk Level: MEDIUM")
                    st.write("You might need to focus more on your studies to avoid falling behind.")
                else:
                    st.error("### Risk Level: HIGH")
                    st.write("Immediate intervention recommended. Please consider increasing study hours and clearing backlogs.")
