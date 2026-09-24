import joblib
import os

RULES_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'skill_rules.pkl')

def load_rules():
    if os.path.exists(RULES_PATH):
        return joblib.load(RULES_PATH)
    return None

def recommend_skills(student_skills):
    """
    Recommend skills based on association rules.
    student_skills: list of strings
    """
    rules = load_rules()
    if rules is None or rules.empty:
        return []

    student_set = set(student_skills)
    recommendations = set()

    for idx, row in rules.iterrows():
        antecedents = set(row['antecedents'])
        consequents = set(row['consequents'])
        
        # If the student has all the antecedent skills
        if antecedents.issubset(student_set):
            # And doesn't already have the consequent skills
            new_skills = consequents - student_set
            recommendations.update(new_skills)

    return list(recommendations)
