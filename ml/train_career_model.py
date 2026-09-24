import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

print("Loading Career Data...")
df = pd.read_csv('data/career_data.csv')

X = df.drop('Role', axis=1)
y = df['Role']

le = LabelEncoder()
y_encoded = le.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Models to compare
rf = RandomForestClassifier(random_state=42)
gb = GradientBoostingClassifier(random_state=42)

print("Training Random Forest...")
rf.fit(X_train, y_train)

print("Training Gradient Boosting...")
gb.fit(X_train, y_train)

print("Training Voting Ensemble...")
voting = VotingClassifier(estimators=[('rf', rf), ('gb', gb)], voting='soft')
voting.fit(X_train, y_train)

# Evaluation function
def evaluate_model(name, model):
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average='weighted')
    rec = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    cm = confusion_matrix(y_test, y_pred)
    print(f"\n--- {name} ---")
    print(f"Accuracy: {acc:.4f} | Precision: {prec:.4f} | Recall: {rec:.4f} | F1: {f1:.4f}")
    print("Confusion Matrix:\n", cm)
    return f1

evaluate_model("Random Forest", rf)
evaluate_model("Gradient Boosting", gb)
best_score = evaluate_model("Voting Ensemble", voting)

# Hyperparameter tuning for Random Forest (as an example of GridSearchCV)
print("\nRunning GridSearchCV for Random Forest...")
param_grid = {'n_estimators': [50, 100], 'max_depth': [None, 10, 20]}
grid = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=3, scoring='f1_weighted')
grid.fit(X_train, y_train)

best_rf = grid.best_estimator_
tuned_score = evaluate_model("Tuned Random Forest", best_rf)

# We'll save the Voting model as it usually generalizes well, but let's check scores
final_model = voting if best_score >= tuned_score else best_rf

joblib.dump(final_model, 'models/career_model.pkl')
joblib.dump(le, 'models/career_le.pkl')
# Save feature names to ensure alignment later
joblib.dump(list(X.columns), 'models/career_features.pkl')

print("\nSaved best model and encoders to models/")
