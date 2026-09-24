import sqlite3
import os

# Path to the database file
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'platform.db')

def get_db_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

def init_db():
    """Initialize the database with tables if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            branch TEXT,
            cgpa REAL,
            attendance REAL,
            year INTEGER,
            career_goal TEXT
        )
    ''')

    # Create student_skills table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            skill TEXT,
            FOREIGN KEY(student_id) REFERENCES students(student_id)
        )
    ''')

    # Create projects table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            title TEXT,
            description TEXT,
            tech_used TEXT,
            FOREIGN KEY(student_id) REFERENCES students(student_id)
        )
    ''')

    # Create certifications table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS certifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            name TEXT,
            issuer TEXT,
            FOREIGN KEY(student_id) REFERENCES students(student_id)
        )
    ''')

    # Create internships table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS internships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            company TEXT,
            role TEXT,
            duration TEXT,
            FOREIGN KEY(student_id) REFERENCES students(student_id)
        )
    ''')

    # Create recruiters table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recruiters (
            recruiter_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            company TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    ''')

    # Create jobs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            job_id INTEGER PRIMARY KEY AUTOINCREMENT,
            recruiter_id INTEGER,
            title TEXT,
            description TEXT,
            required_skills TEXT,
            min_cgpa REAL,
            type TEXT,
            FOREIGN KEY(recruiter_id) REFERENCES recruiters(recruiter_id)
        )
    ''')

    # Create applications table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            app_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            job_id INTEGER,
            match_score REAL,
            status TEXT,
            FOREIGN KEY(student_id) REFERENCES students(student_id),
            FOREIGN KEY(job_id) REFERENCES jobs(job_id)
        )
    ''')

    # Create predictions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            predicted_role TEXT,
            risk_level TEXT,
            date TEXT,
            FOREIGN KEY(student_id) REFERENCES students(student_id)
        )
    ''')

    conn.commit()
    conn.close()

def seed_db():
    """Seed the database with sample data for testing."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if there is already data
    cursor.execute("SELECT COUNT(*) FROM students")
    if cursor.fetchone()[0] > 0:
        print("Database already seeded. Skipping seed process.")
        conn.close()
        return

    # Seed Students
    cursor.execute("INSERT INTO students (name, email, branch, cgpa, attendance, year, career_goal) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                   ('Alice Smith', 'alice@example.com', 'Computer Science', 8.5, 90.0, 3, 'Data Scientist'))
    student_id = cursor.lastrowid
    
    # Seed Skills
    cursor.executemany("INSERT INTO student_skills (student_id, skill) VALUES (?, ?)", 
                       [(student_id, 'Python'), (student_id, 'Pandas'), (student_id, 'Machine Learning')])

    # Seed Recruiter
    cursor.execute("INSERT INTO recruiters (name, company, email) VALUES (?, ?, ?)", 
                   ('Bob Recruiter', 'Tech Corp', 'bob@techcorp.com'))
    recruiter_id = cursor.lastrowid

    # Seed Jobs
    cursor.execute("INSERT INTO jobs (recruiter_id, title, description, required_skills, min_cgpa, type) VALUES (?, ?, ?, ?, ?, ?)", 
                   (recruiter_id, 'Junior Data Scientist', 'Looking for entry level DS.', 'Python, Pandas, Machine Learning', 8.0, 'Full-time'))
    job_id = cursor.lastrowid

    conn.commit()
    conn.close()
    print("Sample data seeded successfully!")

if __name__ == '__main__':
    print("Initializing Database...")
    init_db()
    print("Seeding Database...")
    seed_db()
    print("Database setup complete.")
