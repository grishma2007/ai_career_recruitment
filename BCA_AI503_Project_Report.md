# Project Report: AI-Powered Student Career & Recruitment Platform
**BCA – AI-503**

---

## 1. Introduction and Problem Definition
**Introduction:**
The transition from academic life to professional careers often lacks targeted guidance, leaving students uncertain about their ideal roles and skill gaps. Simultaneously, recruiters struggle to filter through numerous applications to find candidates whose skills genuinely match job requirements.

**Problem Definition:**
There is a need for an intelligent system that can assess a student's academic and skill profile to predict suitable career paths, identify academic risks early, and seamlessly connect qualified students with relevant job postings using data-driven matching algorithms.

## 2. Dataset Collection and Understanding
**Dataset Generation:**
Since real-world student academic and recruitment data is sensitive, synthetic datasets were generated using Python (`pandas`, `numpy`, `random`). 
Three primary datasets were created:
1. `career_data.csv`: Contains 1000 records of students' skills (one-hot encoded) and CGPA mapped to 10 different roles (e.g., Data Scientist, Graphic Designer, HR Manager).
2. `risk_data.csv`: Contains 600 records mapping academic metrics (Attendance, Internal Marks, Study Hours, Backlogs, CGPA) to a Risk Level (Low, Medium, High).
3. `skill_transactions.csv`: Contains 600 records of lists of skills possessed by students to discover frequent itemsets and association rules.

**Understanding:**
The features represent real-world metrics (e.g., attendance percentages, CGPA on a 10-point scale, binary presence of skills). The target variables are categorical (Role, Risk Level).

## 3. Data Preprocessing
Data preprocessing involved several steps to prepare the synthetic data for machine learning:
- **Encoding Categorical Targets**: The `LabelEncoder` from `scikit-learn` was used to transform string labels (like 'Data Scientist' or 'High Risk') into numerical formats required by the algorithms.
- **Feature Selection**: Separating the input features (X) from the target labels (y).
- **Train-Test Split**: The datasets were split into training (80%) and testing (20%) sets to evaluate model generalization.
- **One-Hot Encoding**: Skill data was naturally structured as one-hot encoded binary vectors (1 if the skill is present, 0 otherwise).

## 4. Machine Learning Model Development
Two primary predictive models were developed:
1. **Career Prediction Model**: Predicts the ideal job role based on skills and CGPA. 
   - Algorithms tested: Random Forest Classifier, Gradient Boosting Classifier.
   - Final Model: A Voting Classifier ensemble combining Random Forest and Gradient Boosting to maximize accuracy and stability.
2. **Academic Risk Predictor**: Predicts the likelihood of academic failure based on attendance, marks, and study habits.
   - Algorithm used: Random Forest Classifier.
3. **Skill Recommender**: Uses the Apriori algorithm from `mlxtend` to find association rules between skills and recommend skills frequently learned together.

## 5. Model Evaluation
The models were evaluated on the test set using standard classification metrics:
- **Accuracy**: To measure overall correctness.
- **Precision, Recall, and F1-Score (Weighted)**: To ensure balanced performance across all classes, especially since multi-class classification is involved.
- **Confusion Matrix**: To visualize true positives against false positives for each specific role and risk level.
*The Career Prediction Voting Ensemble achieved an accuracy of ~94%, while the Risk Predictor achieved high precision on classifying "High Risk" students.*

## 6. Model Saving and Serialization
To deploy the models efficiently without retraining them on every request, they were serialized using the `joblib` library.
- The trained classifiers (`career_model.pkl`, `risk_model.pkl`) were exported to the `models/` directory.
- The `LabelEncoder` objects (`career_le.pkl`, `risk_le.pkl`) were also saved to map the numerical predictions back to human-readable strings during inference.
- Feature names (`career_features.pkl`) were saved to ensure the input data array aligns perfectly with the model's expected shape during API requests.

## 7. API Development using Flask/FastAPI
A RESTful backend API was developed using **Flask** to separate the machine learning and database logic from the user interface.
- **Endpoints**: Include `/predict_career`, `/predict_risk`, `/match_jobs`, and standard CRUD endpoints for students and jobs.
- **Data Exchange**: Uses JSON format for request payloads and responses.
- **Database Integration**: SQLite3 is connected via Flask routes to store and retrieve persistent user data, skills, and applications.
- **Global Model Loading**: Machine learning models are loaded into memory once when the Flask server starts to ensure fast, low-latency predictions.

## 8. User Interface Development
The frontend was developed using **Streamlit**, a Python framework ideal for building data-focused web applications rapidly.
- **Multi-page Architecture**: The app uses `st.navigation` to organize distinct pages (Student Profile, Job Posting, Career Prediction, Academic Risk, Dashboards).
- **Session State**: `st.session_state` is heavily utilized to manage temporary user data (like logged-in Student ID and role toggling) without requiring a complex authentication system.
- **Interactive Elements**: Utilizes forms, sliders, select boxes, and dynamic text inputs to collect user data intuitively.

## 9. Model Deployment and Prediction
The complete system is deployed as a decoupled architecture on the local machine:
1. The Flask API runs on `localhost:5000`, continuously listening for HTTP POST requests containing user data.
2. The Streamlit App runs on a separate port (`8501`).
3. **Prediction Flow**: When a student clicks "Predict Ideal Career Role", the Streamlit app packages their skills and CGPA into a JSON payload and sends it via the `requests` library to the Flask `/predict_career` endpoint. The Flask server deserializes the model, runs `model.predict()`, and returns the predicted string label to be displayed on the UI.

## 10. Input / Output Screen Layout
- **Student Profile (Input)**: A form containing text fields for Name/Email, dropdowns for Branch/Year, sliders for CGPA/Attendance, and a multi-select box for Skills.
- **Career Prediction (Output)**: Displays a success banner with the predicted role (e.g., "Graphic Designer") and a bar chart visualizing the confidence distribution across different roles.
- **Job Matching (Output)**: An expandable list of jobs sorted by their percentage match score, with an inline "Apply" button.
- **Candidate Ranking (Output)**: A data table for recruiters showing applicants sorted by match score and CGPA.

## 11. Future Enhancements
- **Authentication System**: Implement JWT-based login using Flask-Security or Firebase for secure user sessions.
- **Natural Language Processing (NLP)**: Integrate deep learning models (like BERT) to analyze open-text resumes and extract skills automatically, replacing the current keyword-matching heuristics.
- **Cloud Deployment**: Containerize the Flask backend and Streamlit frontend using Docker and deploy them to AWS, Heroku, or GCP.
- **Real-Time Notifications**: Add email alerts to notify students when they are matched with a new job.

## 12. Conclusion
The AI-Powered Student Career & Recruitment Platform successfully demonstrates how machine learning can be integrated into a web application to solve real-world educational and HR challenges. By combining scikit-learn for intelligent predictions, Flask for robust API handling, and Streamlit for an interactive UI, the project provides a seamless, end-to-end experience for both students and recruiters.

## 13. References
1. Python Documentation: https://docs.python.org/3/
2. Scikit-Learn Documentation: https://scikit-learn.org/stable/
3. Flask Documentation: https://flask.palletsprojects.com/
4. Streamlit Documentation: https://docs.streamlit.io/

## 14. Bibliography
- McKinney, W. (2012). *Python for Data Analysis*. O'Reilly Media, Inc.
- Grinberg, M. (2018). *Flask Web Development: Developing Web Applications with Python*. O'Reilly Media, Inc.
- Müller, A. C., & Guido, S. (2016). *Introduction to Machine Learning with Python*. O'Reilly Media, Inc.
