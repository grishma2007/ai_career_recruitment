# Project Report: AI-Powered Student Career & Recruitment Platform

## 1. Objectives
The primary objective of this project is to bridge the gap between academic preparation and industry requirements. The platform serves two distinct users:
1. **Students**: Provide actionable AI-driven guidance on career paths, highlight skill gaps, evaluate academic risk, and match them seamlessly with relevant job opportunities.
2. **Recruiters**: Streamline the hiring process by allowing them to post targeted jobs and instantly view applicants ranked by their compatibility with the job requirements.

## 2. Architecture & Tech Stack
The project follows a standard decoupled Client-Server architecture:
- **Frontend (Client)**: Built with **Streamlit** to leverage its rapid prototyping capabilities for data-driven web applications. It utilizes a multi-page structure and `session_state` to handle the dual-role system ("Student" vs "Recruiter") without complex authentication overhead.
- **Backend (Server)**: A **Flask REST API** handles all business logic, data persistence, and model inference. It exposes clean JSON endpoints.
- **Database**: **SQLite** is used as a lightweight, serverless relational database to store users, skills, jobs, and applications.
- **Machine Learning**: Standard Python data science stack (**Pandas, Numpy, Scikit-Learn, mlxtend**).

## 3. Core Modules
- **Resume Parser Module**: A lightweight text parser that matches raw input text against a predefined `skills_master.csv` list to extract technical skills.
- **Job Matching Module**: Calculates a precise percentage match by computing the intersection of a candidate's skill set and the job's required skill set.
- **Career Prediction (ML)**: Uses a Voting Classifier (combining Random Forest and Gradient Boosting) trained on synthetic data mapping skills and CGPA to 6 distinct job roles (e.g., Data Scientist, Backend Developer). Tuned via GridSearchCV.
- **Academic Risk Assessor (ML)**: Predicts "Low", "Medium", or "High" academic risk using metrics such as attendance, study hours, and current backlogs, allowing early intervention.
- **Recommendation Engine**: Implements the FP-Growth algorithm (via `mlxtend`) to mine frequent itemsets from historical skill transactions, generating confident association rules (e.g., "If React & Node.js -> Learn MongoDB").

## 4. Results & Outcomes
- **Model Performance**: The Career Prediction and Risk Assessment models achieved high F1-scores (>0.85) on the synthetic datasets, validating the feature engineering approach.
- **Rule Mining**: Over 900 strong association rules were generated, successfully powering the dynamic skill recommendation engine.
- **System Integration**: Both the Flask backend and Streamlit frontend integrate perfectly, executing near-instant API calls and demonstrating a complete, working end-to-end recruitment flow.

## 5. Future Enhancements
- Integration with NLP libraries (e.g., spaCy) for robust contextual resume parsing.
- Implementation of a real authentication system (JWT/OAuth).
- Use of cloud databases (PostgreSQL) and deployment via Docker/AWS.
