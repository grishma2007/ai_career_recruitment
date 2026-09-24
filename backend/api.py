from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import joblib
import pandas as pd
import sqlite3

import sys
sys.path.insert(0, os.path.dirname(__file__))

# Import our custom modules
from database import get_db_connection, init_db, seed_db
from validators import validate_json
from resume_parser import extract_skills_from_text
from matching import match_student_to_job
from recommender import recommend_skills

app = Flask(__name__)
CORS(app)

# Ensure database is initialized
init_db()
seed_db()

# Load Models globally
MODELS_DIR = os.path.join(os.path.dirname(__file__), '..', 'models')
try:
    career_model = joblib.load(os.path.join(MODELS_DIR, 'career_model.pkl'))
    career_le = joblib.load(os.path.join(MODELS_DIR, 'career_le.pkl'))
    career_features = joblib.load(os.path.join(MODELS_DIR, 'career_features.pkl'))
    
    risk_model = joblib.load(os.path.join(MODELS_DIR, 'risk_model.pkl'))
    risk_le = joblib.load(os.path.join(MODELS_DIR, 'risk_le.pkl'))
    risk_features = joblib.load(os.path.join(MODELS_DIR, 'risk_features.pkl'))
except Exception as e:
    print(f"Warning: Models not loaded. Please ensure Phase 2 completed. Error: {e}")

# --- ML ENDPOINTS ---

@app.route('/predict_career', methods=['POST'])
def predict_career():
    data = request.json
    valid, msg = validate_json(data, ['skills', 'cgpa'])
    if not valid: return jsonify({"error": msg}), 400

    skills = data['skills']
    cgpa = data['cgpa']

    # Build input array
    input_dict = {f: 0 for f in career_features}
    input_dict['CGPA'] = cgpa
    for skill in skills:
        if skill in input_dict:
            input_dict[skill] = 1

    input_df = pd.DataFrame([input_dict])
    pred = career_model.predict(input_df)
    role = career_le.inverse_transform(pred)[0]

    return jsonify({"predicted_role": role})

@app.route('/predict_risk', methods=['POST'])
def predict_risk():
    data = request.json
    required = ['attendance', 'internal_marks', 'study_hours', 'backlogs', 'cgpa']
    valid, msg = validate_json(data, required)
    if not valid: return jsonify({"error": msg}), 400

    input_dict = {
        'Attendance': data['attendance'],
        'Internal_Marks': data['internal_marks'],
        'Study_Hours': data['study_hours'],
        'Backlogs': data['backlogs'],
        'CGPA': data['cgpa']
    }
    input_df = pd.DataFrame([input_dict])
    pred = risk_model.predict(input_df)
    risk = risk_le.inverse_transform(pred)[0]

    return jsonify({"risk_level": risk})

@app.route('/extract_skills', methods=['POST'])
def extract_skills():
    data = request.json
    valid, msg = validate_json(data, ['text'])
    if not valid: return jsonify({"error": msg}), 400

    skills = extract_skills_from_text(data['text'])
    return jsonify({"skills": skills})

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    valid, msg = validate_json(data, ['skills'])
    if not valid: return jsonify({"error": msg}), 400

    recommended = recommend_skills(data['skills'])
    return jsonify({"recommended_skills": list(recommended)})

@app.route('/match_jobs', methods=['POST'])
def match_jobs():
    data = request.json
    valid, msg = validate_json(data, ['skills', 'cgpa'])
    if not valid: return jsonify({"error": msg}), 400
    
    student_skills = data['skills']
    cgpa = data['cgpa']

    conn = get_db_connection()
    jobs = conn.execute("SELECT * FROM jobs").fetchall()
    conn.close()

    matches = []
    for job in jobs:
        req_skills = [s.strip() for s in job['required_skills'].split(',')]
        if cgpa >= job['min_cgpa']:
            score = match_student_to_job(student_skills, req_skills)
            matches.append({
                "job_id": job['job_id'],
                "title": job['title'],
                "company_id": job['recruiter_id'], # simplified for now
                "required_skills": job['required_skills'],
                "match_score": score
            })
            
    matches.sort(key=lambda x: x['match_score'], reverse=True)
    return jsonify({"matches": matches})

# --- CRUD ENDPOINTS ---

@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    conn = get_db_connection()
    # Delete related records first
    conn.execute("DELETE FROM student_skills WHERE student_id=?", (student_id,))
    conn.execute("DELETE FROM applications WHERE student_id=?", (student_id,))
    # Delete the student
    cursor = conn.execute("DELETE FROM students WHERE student_id=?", (student_id,))
    conn.commit()
    conn.close()
    
    if cursor.rowcount == 0:
        return jsonify({"error": "Student not found"}), 404
    return jsonify({"message": "Profile deleted successfully"}), 200

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    conn = get_db_connection()
    student = conn.execute("SELECT * FROM students WHERE student_id=?", (student_id,)).fetchone()
    if not student:
        conn.close()
        return jsonify({"error": "Student not found"}), 404
    
    skills_rows = conn.execute("SELECT skill FROM student_skills WHERE student_id=?", (student_id,)).fetchall()
    skills = [row['skill'] for row in skills_rows]
    conn.close()
    
    student_dict = dict(student)
    student_dict['skills'] = skills
    return jsonify(student_dict)

@app.route('/students', methods=['GET'])
def get_students():
    conn = get_db_connection()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return jsonify([dict(s) for s in students])

@app.route('/students', methods=['POST'])
def create_student():
    data = request.json
    valid, msg = validate_json(data, ['name', 'email', 'cgpa'])
    if not valid: return jsonify({"error": msg}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, email, branch, cgpa, attendance, year, career_goal) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (data['name'], data['email'], data.get('branch',''), data['cgpa'], data.get('attendance',0), data.get('year',1), data.get('career_goal','')))
        student_id = cursor.lastrowid
        
        skills = data.get('skills', [])
        for skill in skills:
            cursor.execute("INSERT INTO student_skills (student_id, skill) VALUES (?, ?)", (student_id, skill))
            
        conn.commit()
        conn.close()
        return jsonify({"student_id": student_id, "message": "Created successfully"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 400

@app.route('/jobs', methods=['GET'])
def get_jobs():
    conn = get_db_connection()
    jobs = conn.execute("SELECT jobs.*, recruiters.company FROM jobs JOIN recruiters ON jobs.recruiter_id = recruiters.recruiter_id").fetchall()
    conn.close()
    return jsonify([dict(j) for j in jobs])

@app.route('/jobs', methods=['POST'])
def create_job():
    data = request.json
    valid, msg = validate_json(data, ['recruiter_id', 'title', 'required_skills'])
    if not valid: return jsonify({"error": msg}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO jobs (recruiter_id, title, description, required_skills, min_cgpa, type) VALUES (?, ?, ?, ?, ?, ?)",
                   (data['recruiter_id'], data['title'], data.get('description',''), data['required_skills'], data.get('min_cgpa',0), data.get('type','Full-time')))
    conn.commit()
    job_id = cursor.lastrowid
    conn.close()
    return jsonify({"job_id": job_id, "message": "Created successfully"}), 201

@app.route('/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    conn = get_db_connection()
    # Delete related applications first
    conn.execute("DELETE FROM applications WHERE job_id=?", (job_id,))
    # Delete the job
    cursor = conn.execute("DELETE FROM jobs WHERE job_id=?", (job_id,))
    conn.commit()
    conn.close()
    
    if cursor.rowcount == 0:
        return jsonify({"error": "Job not found"}), 404
    return jsonify({"message": "Job deleted successfully"}), 200

@app.route('/applications', methods=['POST'])
def apply_job():
    data = request.json
    valid, msg = validate_json(data, ['student_id', 'job_id', 'match_score'])
    if not valid: return jsonify({"error": msg}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    # Check if already applied
    existing = cursor.execute("SELECT * FROM applications WHERE student_id=? AND job_id=?", (data['student_id'], data['job_id'])).fetchone()
    if existing:
        return jsonify({"error": "Already applied to this job."}), 400

    cursor.execute("INSERT INTO applications (student_id, job_id, match_score, status) VALUES (?, ?, ?, ?)",
                   (data['student_id'], data['job_id'], data['match_score'], 'Applied'))
    conn.commit()
    conn.close()
    return jsonify({"message": "Application submitted."}), 201

@app.route('/rank_candidates/<int:job_id>', methods=['GET'])
def rank_candidates(job_id):
    conn = get_db_connection()
    query = '''
        SELECT students.name, students.email, students.cgpa, applications.match_score, applications.status
        FROM applications
        JOIN students ON applications.student_id = students.student_id
        WHERE applications.job_id = ?
        ORDER BY applications.match_score DESC, students.cgpa DESC
    '''
    candidates = conn.execute(query, (job_id,)).fetchall()
    conn.close()
    return jsonify([dict(c) for c in candidates])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
