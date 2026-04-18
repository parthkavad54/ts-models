import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import warnings
warnings.filterwarnings('ignore')

def main():
    print("Loading data from c:/Users/HELLO/Desktop/MODEL/TS-PS12.csv...")
    df = pd.read_csv("c:/Users/HELLO/Desktop/MODEL/TS-PS12.csv")

    X = df[['attendance', 'marks', 'assignment', 'lms']]
    y = df['risk_label']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training RandomForestClassifier...")
    # STRICT MAX LIMITS to strictly cap the .pkl file size under GitHub's 100MB limit
    model = RandomForestClassifier(n_estimators=30, max_depth=8, random_state=42)
    model.fit(X_train, y_train)

    print("Evaluating model...")
    y_pred = model.predict(X_test)
    print(f"\nAccuracy: {accuracy_score(y_test, y_pred)}\n")
    print(classification_report(y_test, y_pred))

    joblib.dump(model, "c:/Users/HELLO/Desktop/MODEL/risk_model.pkl")
    print("Training complete! Model saved.")

if __name__ == "__main__":
    main()
