import requests

BASE_URL = "http://localhost:5000"

def test_endpoint(name, method, path, data=None):
    url = f"{BASE_URL}{path}"
    print(f"\n--- Testing {name} ---")
    try:
        if method == "GET":
            response = requests.get(url)
        else:
            response = requests.post(url, json=data)
        
        print(f"Status: {response.status_code}")
        print("Response:", response.json())
    except Exception as e:
        print("Error:", e)

if __name__ == '__main__':
    print("Running API Tests...")
    test_endpoint("Predict Career", "POST", "/predict_career", {"skills": ["Python", "Pandas", "SQL"], "cgpa": 8.5})
    test_endpoint("Predict Risk", "POST", "/predict_risk", {"attendance": 90, "internal_marks": 85, "study_hours": 20, "backlogs": 0, "cgpa": 8.5})
    test_endpoint("Extract Skills", "POST", "/extract_skills", {"text": "I am proficient in Python and React."})
    test_endpoint("Recommend Skills", "POST", "/recommend", {"skills": ["React", "HTML"]})
    test_endpoint("Match Jobs", "POST", "/match_jobs", {"skills": ["Python", "Pandas"], "cgpa": 8.5})
    test_endpoint("Get Students", "GET", "/students")
    test_endpoint("Get Jobs", "GET", "/jobs")
    test_endpoint("Rank Candidates", "GET", "/rank_candidates/1")
