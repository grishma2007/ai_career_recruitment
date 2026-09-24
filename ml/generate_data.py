import pandas as pd
import numpy as np
import random
import os

# Create directories if they don't exist
os.makedirs('data', exist_ok=True)
os.makedirs('models', exist_ok=True)

# 1. Generate Career Data
roles = [
    'Data Scientist', 'Machine Learning Engineer', 'Data Analyst', 'AI Engineer', 
    'Data Engineer', 'Software Developer', 'Full Stack Developer', 'Web Developer', 
    'Backend Developer', 'QA / Software Tester', 'Cybersecurity Analyst', 
    'Cloud / DevOps Engineer', 'Business Analyst', 'UI/UX Designer', 
    'Graphic Designer', 'Digital Marketing Specialist', 'HR Manager', 
    'Sales Executive', 'Product Associate', 'Content Creator',
    'HR Executive', 'Recruiter', 'Business Development Executive', 
    'Marketing Executive', 'Digital Marketing Executive', 'Customer Support Executive', 
    'Operations Executive', 'Finance / Accounts Executive', 'Event Coordinator'
]
skills = [
    'Python', 'SQL', 'Machine Learning', 'Statistics', 'Pandas', 'Data Visualization', 'Mathematics', 
    'Deep Learning', 'TensorFlow', 'Git', 'Excel', 'Power BI', 'NLP', 'Computer Vision', 
    'Database Management', 'ETL', 'Apache Spark', 'Cloud Computing', 'Java', 'C++', 'OOP', 
    'Problem Solving', 'HTML', 'CSS', 'JavaScript', 'React', 'Node.js', 'Express.js', 'MongoDB', 
    'REST API', 'Software Testing', 'Selenium', 'API Testing', 'Cybersecurity', 'Networking', 'Linux', 
    'Ethical Hacking', 'Cryptography', 'AWS', 'Docker', 'Kubernetes', 'CI/CD', 'Business Analysis', 
    'Communication', 'UI/UX Design', 'Figma', 'Adobe XD', 'Wireframing', 'Prototyping', 'User Research', 
    'Graphic Design', 'Photoshop', 'Illustrator', 'Canva', 'Creativity', 'Digital Marketing', 'SEO', 
    'Social Media Marketing', 'Google Analytics', 'Content Writing', 'Human Resources', 'Leadership', 
    'Recruitment', 'Team Management', 'Sales', 'Negotiation', 'CRM', 'Customer Relationship', 
    'Marketing', 'Product Management', 'Market Research', 'Data Analysis', 'Project Management', 
    'Content Creation', 'Video Editing', 'HRMS', 'Documentation', 'Candidate Sourcing', 'Screening', 
    'Interviewing', 'Lead Generation', 'Persuasion', 'Customer Handling', 'Campaign Planning', 'Branding', 
    'Social Media', 'Active Listening', 'Customer Service', 'Coordination', 'Process Management', 
    'Accounting', 'Tally/ERP', 'GST Basics', 'Financial Reporting', 'Event Planning', 'Budgeting', 'Time Management', 'Content Marketing'
]

def generate_career_record():
    role = random.choice(roles)
    record = {skill: 0 for skill in skills}
    
    role_skills_map = {
        'Data Scientist': ['Python', 'SQL', 'Machine Learning', 'Statistics', 'Pandas', 'Data Visualization', 'Mathematics'],
        'Machine Learning Engineer': ['Python', 'Machine Learning', 'Deep Learning', 'TensorFlow', 'SQL', 'Git', 'Mathematics'],
        'Data Analyst': ['SQL', 'Excel', 'Python', 'Pandas', 'Statistics', 'Data Visualization', 'Power BI'],
        'AI Engineer': ['Python', 'Machine Learning', 'Deep Learning', 'TensorFlow', 'NLP', 'Computer Vision', 'Mathematics'],
        'Data Engineer': ['Python', 'SQL', 'Database Management', 'ETL', 'Apache Spark', 'Cloud Computing', 'Git'],
        'Software Developer': ['Python', 'Java', 'C++', 'SQL', 'OOP', 'Git', 'Problem Solving'],
        'Full Stack Developer': ['HTML', 'CSS', 'JavaScript', 'React', 'Node.js', 'Express.js', 'MongoDB', 'Git'],
        'Web Developer': ['HTML', 'CSS', 'JavaScript', 'React', 'Node.js', 'SQL', 'Git'],
        'Backend Developer': ['Python', 'Java', 'Node.js', 'Express.js', 'SQL', 'MongoDB', 'REST API', 'Git'],
        'QA / Software Tester': ['Software Testing', 'Selenium', 'SQL', 'Python', 'Java', 'API Testing', 'Git'],
        'Cybersecurity Analyst': ['Cybersecurity', 'Networking', 'Linux', 'Ethical Hacking', 'Python', 'Cryptography', 'Problem Solving'],
        'Cloud / DevOps Engineer': ['Cloud Computing', 'AWS', 'Docker', 'Kubernetes', 'Linux', 'Git', 'CI/CD'],
        'Business Analyst': ['Excel', 'SQL', 'Data Visualization', 'Business Analysis', 'Communication', 'Problem Solving', 'Power BI'],
        'UI/UX Designer': ['UI/UX Design', 'Figma', 'Adobe XD', 'Wireframing', 'Prototyping', 'User Research', 'Communication'],
        'Graphic Designer': ['Graphic Design', 'Photoshop', 'Illustrator', 'Canva', 'Figma', 'Creativity', 'Communication'],
        'Digital Marketing Specialist': ['Digital Marketing', 'SEO', 'Social Media Marketing', 'Google Analytics', 'Content Writing', 'Communication', 'Canva'],
        'HR Manager': ['Human Resources', 'Communication', 'Leadership', 'Recruitment', 'Team Management', 'Excel', 'Problem Solving'],
        'Sales Executive': ['Sales', 'Communication', 'Negotiation', 'CRM', 'Customer Relationship', 'Marketing', 'Leadership'],
        'Product Associate': ['Product Management', 'Communication', 'Market Research', 'Data Analysis', 'Project Management', 'Problem Solving', 'Leadership'],
        'Content Creator': ['Content Creation', 'Content Writing', 'Social Media Marketing', 'Video Editing', 'Canva', 'Creativity', 'Communication'],
        'HR Executive': ['Communication', 'Recruitment', 'Excel', 'HRMS', 'Documentation'],
        'Recruiter': ['Communication', 'Candidate Sourcing', 'Screening', 'Interviewing', 'Negotiation'],
        'Business Development Executive': ['Communication', 'Sales', 'Lead Generation', 'Negotiation', 'CRM'],
        'Marketing Executive': ['Market Research', 'Communication', 'Campaign Planning', 'Branding', 'Excel'],
        'Digital Marketing Executive': ['SEO', 'Social Media', 'Content Marketing', 'Google Analytics', 'Communication'],
        'Customer Support Executive': ['Communication', 'Active Listening', 'Problem Solving', 'CRM', 'Customer Service'],
        'Operations Executive': ['Excel', 'Coordination', 'Process Management', 'Documentation', 'Problem Solving'],
        'Finance / Accounts Executive': ['Accounting', 'Excel', 'Tally/ERP', 'GST Basics', 'Financial Reporting'],
        'Event Coordinator': ['Event Planning', 'Communication', 'Coordination', 'Budgeting', 'Time Management']
    }
    
    primary_skills = role_skills_map.get(role, [])
    for skill in primary_skills:
        if random.random() < 0.8:
            record[skill] = 1

    cgpa = round(random.uniform(5.5, 10.0), 2)

    # Random noise
    for s in skills:
        if random.random() < 0.15:
            record[s] = 1

    record['CGPA'] = cgpa
    record['Role'] = role
    return record

career_data = [generate_career_record() for _ in range(10000)]
df_career = pd.DataFrame(career_data)
df_career.to_csv('data/career_data.csv', index=False)
print("Generated career_data.csv with 10000 rows.")

# 2. Generate Risk Data
def generate_risk_record():
    risk = random.choice(['Low', 'Medium', 'High'])
    if risk == 'Low':
        attendance = round(random.uniform(85, 100), 2)
        internal_marks = round(random.uniform(75, 100), 2)
        study_hours = round(random.uniform(15, 30), 2)
        backlogs = random.choice([0, 0, 0, 1])
        cgpa = round(random.uniform(8.0, 10.0), 2)
    elif risk == 'Medium':
        attendance = round(random.uniform(70, 85), 2)
        internal_marks = round(random.uniform(55, 75), 2)
        study_hours = round(random.uniform(8, 15), 2)
        backlogs = random.choice([0, 1, 2])
        cgpa = round(random.uniform(6.0, 8.0), 2)
    else:
        attendance = round(random.uniform(40, 70), 2)
        internal_marks = round(random.uniform(30, 55), 2)
        study_hours = round(random.uniform(0, 8), 2)
        backlogs = random.choice([1, 2, 3, 4, 5])
        cgpa = round(random.uniform(4.0, 6.0), 2)
    
    return {
        'Attendance': attendance,
        'Internal_Marks': internal_marks,
        'Study_Hours': study_hours,
        'Backlogs': backlogs,
        'CGPA': cgpa,
        'Risk_Level': risk
    }

risk_data = [generate_risk_record() for _ in range(600)]
df_risk = pd.DataFrame(risk_data)
df_risk.to_csv('data/risk_data.csv', index=False)
print("Generated risk_data.csv with 600 rows.")

# 3. Generate Skill Transactions (for Association Rules)
transactions = []
master_skills = skills

for _ in range(600):
    num_skills = random.randint(2, 6)
    student_skills = random.sample(master_skills, num_skills)
    # Add strong associations (e.g. if React then HTML, CSS)
    if 'React' in student_skills:
        if 'HTML' not in student_skills: student_skills.append('HTML')
        if 'CSS' not in student_skills: student_skills.append('CSS')
    if 'Machine Learning' in student_skills or 'Pandas' in student_skills:
        if 'Python' not in student_skills: student_skills.append('Python')
    transactions.append(student_skills)

with open('data/skill_transactions.csv', 'w') as f:
    for t in transactions:
        f.write(",".join(t) + "\n")
print("Generated skill_transactions.csv with 600 rows.")
