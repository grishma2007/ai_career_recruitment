import requests

BASE_URL = "http://127.0.0.1:5000"

def _post(endpoint, json_data):
    try:
        response = requests.post(f"{BASE_URL}/{endpoint}", json=json_data)
        if response.status_code != 200 and response.status_code != 201:
            return response.json() # return the custom JSON error from the backend
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def _get(endpoint):
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}")
        if response.status_code != 200:
            return response.json()
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def _delete(endpoint):
    try:
        response = requests.delete(f"{BASE_URL}/{endpoint}")
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def create_student(data): return _post("students", data)
def get_jobs(): return _get("jobs")
def get_students(): return _get("students")
def get_student(student_id): return _get(f"students/{student_id}")
def delete_student(student_id): return _delete(f"students/{student_id}")
def apply_job(student_id, job_id, match_score): 
    return _post("applications", {"student_id": student_id, "job_id": job_id, "match_score": match_score})
def predict_career(skills, cgpa): return _post("predict_career", {"skills": skills, "cgpa": cgpa})
def predict_risk(data): return _post("predict_risk", data)
def extract_skills(text): return _post("extract_skills", {"text": text})
def recommend_skills(skills): return _post("recommend", {"skills": skills})
def match_jobs(skills, cgpa): return _post("match_jobs", {"skills": skills, "cgpa": cgpa})
def create_job(data): return _post("jobs", data)
def rank_candidates(job_id): return _get(f"rank_candidates/{job_id}")
