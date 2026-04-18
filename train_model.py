import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

def main():
    dataset_path = "c:/Users/HELLO/Desktop/MODEL/TS-PS12.csv"
    model_path = "c:/Users/HELLO/Desktop/MODEL/risk_model.pkl"
    
    print(f"Loading data from {dataset_path}...")
    df = pd.read_csv(dataset_path)

    # Features and Target
    X = df[['attendance', 'marks', 'assignment', 'lms']]
    
    # We can train on 'risk_label' (classification) or 'risk_score' (regression)
    # Let's do classification on 'risk_label'
    y = df['risk_label']

    print(f"Data Loaded. Shape: {df.shape}")
    print("Splitting dataset into training and testing sets...")
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training RandomForestClassifier...")
    model = RandomForestClassifier(random_state=42, n_estimators=100)
    model.fit(X_train, y_train)

    print("Evaluating model...")
    y_pred = model.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    print(f"\nAccuracy: {acc:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    print(f"Saving trained model to {model_path}...")
    joblib.dump(model, model_path)
    print("Training complete!")

if __name__ == "__main__":
    main()
