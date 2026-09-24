import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

print("Loading Risk Data...")
df = pd.read_csv('data/risk_data.csv')

X = df.drop('Risk_Level', axis=1)
y = df['Risk_Level']

le = LabelEncoder()
y_encoded = le.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

rf = RandomForestClassifier(random_state=42)
gb = GradientBoostingClassifier(random_state=42)
voting = VotingClassifier(estimators=[('rf', rf), ('gb', gb)], voting='soft')

print("Training Models...")
rf.fit(X_train, y_train)
gb.fit(X_train, y_train)
voting.fit(X_train, y_train)

def evaluate_model(name, model):
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    cm = confusion_matrix(y_test, y_pred)
    print(f"\n--- {name} ---")
    print(f"Accuracy: {acc:.4f} | Precision: {prec:.4f} | Recall: {rec:.4f} | F1: {f1:.4f}")
    print("Confusion Matrix:\n", cm)
    return f1

evaluate_model("Random Forest", rf)
evaluate_model("Gradient Boosting", gb)
best_score = evaluate_model("Voting Ensemble", voting)

# GridSearchCV for GB
print("\nRunning GridSearchCV for Gradient Boosting...")
param_grid = {'n_estimators': [50, 100], 'learning_rate': [0.05, 0.1]}
grid = GridSearchCV(GradientBoostingClassifier(random_state=42), param_grid, cv=3, scoring='f1_weighted')
grid.fit(X_train, y_train)

best_gb = grid.best_estimator_
tuned_score = evaluate_model("Tuned Gradient Boosting", best_gb)

final_model = voting if best_score >= tuned_score else best_gb

joblib.dump(final_model, 'models/risk_model.pkl')
joblib.dump(le, 'models/risk_le.pkl')
joblib.dump(list(X.columns), 'models/risk_features.pkl')

print("\nSaved best model and encoders to models/")
