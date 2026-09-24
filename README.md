# AI-Powered Student Career & Recruitment Platform

A comprehensive two-sided platform designed to help students discover their ideal career paths, mitigate academic risks, and find the perfect job matches. On the flip side, it allows recruiters to post job openings and discover top-ranked candidates tailored to their needs.

## Features

### For Students
- **Resume Analyzer**: Paste raw resume text to extract key technical skills using keyword matching.
- **Career Prediction**: Predict your ideal career role (e.g., Data Scientist, Backend Developer) using an ML Voting Ensemble based on skills and CGPA.
- **Academic Risk Predictor**: Evaluate your academic trajectory to determine if you are at Low, Medium, or High risk based on attendance, study hours, and backlogs.
- **Learning Recommendations**: Get data-driven recommendations on what skills to learn next using Apriori Association Rules.
- **Job Matching & Dashboard**: View jobs matched to your profile with a percentage score and apply instantly.

### For Recruiters
- **Post Jobs**: Create job listings with required skills and minimum CGPA.
- **Candidate Ranking**: View all applicants for a specific role, intelligently ranked by their AI match score and CGPA.
- **Dashboard Management**: Shortlist or reject candidates directly from the recruiter dashboard.

## Tech Stack
- **Frontend**: Streamlit (Multi-page app architecture)
- **Backend**: Flask REST API (flask-cors)
- **Database**: SQLite3
- **Machine Learning**: Scikit-Learn (Random Forest, Gradient Boosting, Voting Ensembles), mlxtend (FP-Growth), Pandas, Numpy, Joblib

---

## Setup & Run Instructions

**1. Prerequisites**
Ensure you have Python 3.8+ installed.

**2. Install Dependencies**
```bash
pip install -r requirements.txt
```

**3. Initialize and Seed the Database**
```bash
python backend/database.py
```

**4. Generate ML Datasets and Train Models**
```bash
python ml/generate_data.py
python ml/train_career_model.py
python ml/train_risk_model.py
python ml/build_association_rules.py
```
*(Note: These scripts are already executed if you pulled the complete repository with `models/` directory intact)*

**5. Start the Application**
You need two terminals to run the platform locally.

**Terminal 1: Start the Backend API**
```bash
python backend/api.py
```
*(Runs on http://localhost:5000)*

**Terminal 2: Start the Frontend App**
```bash
streamlit run app.py
```
*(Runs on http://localhost:8501)*

## Architecture
- **`app.py` & `pages/`**: Streamlit frontend controlling the UI and role switching.
- **`backend/`**: Flask API endpoints, database initialization, ML model loading, and business logic (resume parsing, matching).
- **`ml/`**: Scripts for data generation, model training, and rule mining.
- **`models/`**: Serialized `.pkl` files representing the trained Scikit-Learn models and LabelEncoders.
- **`data/`**: SQLite database (`platform.db`), raw CSV datasets, and the skill master list.
