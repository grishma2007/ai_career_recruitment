def match_student_to_job(student_skills, required_skills):
    """
    Calculate a match score between a student's skills and job's required skills.
    student_skills: list of strings
    required_skills: list of strings
    Returns: float (0 to 100)
    """
    if not required_skills:
        return 100.0  # No skills required means perfect match
        
    student_set = set([s.lower().strip() for s in student_skills])
    required_set = set([s.lower().strip() for s in required_skills])
    
    intersection = student_set.intersection(required_set)
    match_score = (len(intersection) / len(required_set)) * 100.0
    
    return round(match_score, 2)
