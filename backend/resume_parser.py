import os

# Load skills from master list
def load_skills_master():
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'skills_master.csv')
    with open(csv_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    return [s.strip().lower() for s in content.split(',')]

MASTER_SKILLS = load_skills_master()

def extract_skills_from_text(text):
    """Extract skills from plain text by checking against the master list."""
    if not text:
        return []
    
    text_lower = text.lower()
    extracted = []
    
    for skill in MASTER_SKILLS:
        # Simple substring matching. For a real app, word boundaries are better.
        if skill in text_lower:
            # Capitalize properly by finding original or just title casing
            extracted.append(skill.title() if skill != 'sql' and skill != 'aws' else skill.upper())
            
    # Clean up exact cases like Node.js
    final_skills = []
    for s in extracted:
        if s.lower() == 'node.js': final_skills.append('Node.js')
        elif s.lower() == 'c++': final_skills.append('C++')
        elif s.lower() == 'html': final_skills.append('HTML')
        elif s.lower() == 'css': final_skills.append('CSS')
        elif s.lower() == 'aws': final_skills.append('AWS')
        elif s.lower() == 'sql': final_skills.append('SQL')
        elif s.lower() == 'mysql': final_skills.append('MySQL')
        else: final_skills.append(s)
            
    return list(set(final_skills))
