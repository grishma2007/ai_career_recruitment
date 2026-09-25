import streamlit as st
import os
# Set page config
st.set_page_config(page_title="AI Career Platform", page_icon="🎓", layout="wide")

# Custom CSS for attractive UI
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Subtle Gradient Text for Main Titles to give an AI vibe */
    h1 {
        background: -webkit-linear-gradient(45deg, #2563EB, #7C3AED);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
        margin-bottom: 1.5rem !important;
        letter-spacing: -0.02em;
    }
    
    /* Headers */
    h2, h3 {
        color: #111827 !important;
        font-weight: 600 !important;
        letter-spacing: -0.01em;
    }
    
    /* General text color */
    .stMarkdown p {
        color: #111827;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #2563EB;
        color: #FFFFFF !important;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1.2rem;
        font-weight: 500;
        transition: all 0.2s ease;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }
    .stButton>button:hover {
        background-color: #1D4ED8;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2), 0 2px 4px -1px rgba(37, 99, 235, 0.1);
        transform: translateY(-1px);
        color: #FFFFFF !important;
    }
    
    /* Inputs */
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea {
        background-color: #FFFFFF !important;
        color: #111827 !important;
        border-radius: 8px !important;
        border: 1px solid #E2E8F0 !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }
    .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus, .stSelectbox>div>div>div:focus, .stTextArea>div>div>textarea:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
    }
    
    /* DataFrames and Tables */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        background-color: #FFFFFF;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #2563EB !important;
        font-weight: 700;
        font-size: 2.2rem !important;
    }
    [data-testid="stMetricLabel"] {
        color: #64748B !important;
        font-weight: 500;
    }
    
    /* Cards (Expanders) */
    .streamlit-expanderHeader {
        background-color: #FFFFFF !important;
        border-radius: 12px !important;
        border: 1px solid #E2E8F0 !important;
        font-weight: 600 !important;
        color: #111827 !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        transition: background-color 0.2s ease;
    }
    .streamlit-expanderHeader:hover {
        background-color: #F8FAFC !important;
    }
    .streamlit-expanderContent {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-top: none !important;
        border-bottom-left-radius: 12px !important;
        border-bottom-right-radius: 12px !important;
        padding-top: 1rem;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0;
    }
    
    /* Info/Success/Warning boxes */
    .stAlert {
        border-radius: 12px !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }
</style>
""", unsafe_allow_html=True)

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
