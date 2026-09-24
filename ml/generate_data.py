import pandas as pd
import numpy as np
import random
import os

# Create directories if they don't exist
os.makedirs('data', exist_ok=True)
os.makedirs('models', exist_ok=True)

# 1. Generate Career Data
roles = ['Data Scientist', 'Web Developer', 'ML Engineer', 'Data Analyst', 'Backend Developer', 'Software Tester', 'Graphic Designer', 'Marketing Manager', 'HR Manager', 'Sales Executive']
skills = ['Python', 'Java', 'SQL', 'React', 'AWS', 'Pandas', 'Node.js', 'Machine Learning', 'Selenium', 'Docker', 'Digital Marketing', 'SEO', 'Content Creation', 'Social Media Management', 'Market Research', 'Talent Acquisition', 'Employee Relations', 'HR Management', 'Project Management', 'Communication', 'Leadership', 'Adobe Photoshop', 'Illustrator', 'Figma', 'Sales', 'B2B']

def generate_career_record():
    role = random.choice(roles)
    record = {skill: 0 for skill in skills}
    
    # Add strong signals for roles
    if role == 'Data Scientist':
        record['Python'] = 1; record['Pandas'] = 1; record['Machine Learning'] = random.choice([0, 1]); record['SQL'] = 1
        cgpa = round(random.uniform(7.5, 10.0), 2)
    elif role == 'Web Developer':
        record['React'] = 1; record['Node.js'] = 1; record['AWS'] = random.choice([0, 1])
        cgpa = round(random.uniform(6.5, 9.5), 2)
    elif role == 'ML Engineer':
        record['Python'] = 1; record['Machine Learning'] = 1; record['Docker'] = 1; record['AWS'] = random.choice([0, 1])
        cgpa = round(random.uniform(8.0, 10.0), 2)
    elif role == 'Data Analyst':
        record['SQL'] = 1; record['Pandas'] = 1; record['Python'] = random.choice([0, 1])
        cgpa = round(random.uniform(6.0, 9.0), 2)
    elif role == 'Backend Developer':
        record['Java'] = 1; record['SQL'] = 1; record['Docker'] = random.choice([0, 1])
        cgpa = round(random.uniform(7.0, 9.5), 2)
    elif role == 'Software Tester':
        record['Selenium'] = 1; record['Python'] = random.choice([0, 1]); record['Java'] = random.choice([0, 1])
        cgpa = round(random.uniform(6.0, 8.5), 2)
    elif role == 'Graphic Designer':
        record['Adobe Photoshop'] = 1; record['Illustrator'] = 1; record['Figma'] = random.choice([0, 1]); record['Content Creation'] = random.choice([0, 1])
        cgpa = round(random.uniform(5.5, 9.0), 2)
    elif role == 'Marketing Manager':
        record['Digital Marketing'] = 1; record['SEO'] = 1; record['Social Media Management'] = random.choice([0, 1]); record['Communication'] = 1
        cgpa = round(random.uniform(6.0, 9.0), 2)
    elif role == 'HR Manager':
        record['HR Management'] = 1; record['Talent Acquisition'] = 1; record['Employee Relations'] = random.choice([0, 1]); record['Communication'] = 1
        cgpa = round(random.uniform(6.0, 9.5), 2)
    elif role == 'Sales Executive':
        record['Sales'] = 1; record['B2B'] = random.choice([0, 1]); record['Communication'] = 1; record['Leadership'] = random.choice([0, 1])
        cgpa = round(random.uniform(5.5, 8.5), 2)

    # Random noise
    for s in skills:
        if random.random() < 0.15:
            record[s] = 1

    record['CGPA'] = cgpa
    record['Role'] = role
    return record

career_data = [generate_career_record() for _ in range(1000)]
df_career = pd.DataFrame(career_data)
df_career.to_csv('data/career_data.csv', index=False)
print("Generated career_data.csv with 1000 rows.")

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
master_skills = ['Python', 'Java', 'SQL', 'React', 'AWS', 'Pandas', 'Node.js', 'Machine Learning', 'Docker', 'HTML', 'CSS', 'Git', 'MongoDB']

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
