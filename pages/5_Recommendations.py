import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils.api_client as api

st.title("Learning Recommendations")

if st.session_state["role"] != 'Student':
    st.warning("Please switch to the Student role to view this page.")
    st.stop()

skills = st.session_state.get('student_skills', [])

if not skills:
    st.warning("You have no skills listed. Please update your profile first.")
    st.stop()

st.write(f"**Your Skills:** {', '.join(skills)}")
st.write("Based on association rules mined from student data, here is what students with similar skills learn next:")

if st.button("Get Recommendations"):
    with st.spinner("Finding recommendations..."):
        res = api.recommend_skills(skills)
        if "error" in res:
            st.error(res["error"])
        else:
            rec = res.get("recommended_skills", [])
            if rec:
                st.success("We found some great next steps for you!")
                for r in rec:
                    st.markdown(f"- **{r}**")
            else:
                st.info("No strong recommendations found for your current skill set. Keep exploring!")
