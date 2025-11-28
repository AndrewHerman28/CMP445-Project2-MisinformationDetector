# predictor.py
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from App.preprocessing import clean_text
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import VotingClassifier
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.metrics import accuracy_score, classification_report

MODEL_PATH = "/Users/andrewherman/CMP445/Project2-MisinformationClassifier/Models/model.pkl"


# --- TRAINING FUNCTION (Run once to create model.pkl) ---
def train_model():
    # Load datasets
    print("Loading data...")
    df = pd.read_csv("/Users/andrewherman/CMP445/Project2-MisinformationClassifier/Data/Processed/merged_data.csv")
    print(df.head())

    # Clean text
    print("Cleaning text...")
    df["title"] = df["title"].fillna("").apply(clean_text)
    df["text"] = df["text"].fillna("").apply(clean_text)
    df["combined"] = df["title"] + " " + df["text"]

    X = df["combined"]
    y = df["hasMisinformation"]

    # train test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # SVM needs calibration for probabilities
    svm_clf = CalibratedClassifierCV(LinearSVC(), cv=5)

    # Simple model pipeline
    print("Training model...")
    ensemble = VotingClassifier(
        estimators=[
            ("lr", LogisticRegression(max_iter=2000)),
            ("nb", MultinomialNB()),
            ("svm", svm_clf),
            ("sgd", SGDClassifier(loss="log_loss"))
        ],
        voting="soft"
    )

    model = Pipeline([
        ("tfidf", TfidfVectorizer(
            stop_words="english",
            max_features=15000,  # increase feature space
            ngram_range=(1, 2),  # unigrams + bigrams
            min_df=3,  # reduce noise
        )),
        ("select", SelectKBest(chi2, k=8000)),  # feature selection
        ("clf", ensemble)
    ])

    # Train model
    model.fit(X_train, y_train)

    # Evaluate model
    preds = model.predict_proba(X_test)
    accuracy = accuracy_score(y_test, preds)
    print(f"\nValidation Accuracy: {accuracy:.4f}")
    print(classification_report(y_test, preds))

    # Save model
    joblib.dump(model, MODEL_PATH)
    print("Model saved to", MODEL_PATH)


# Run once to create model.pkl
# train_model()


# --- LOAD MODEL ---
def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Model not trained yet. Run train_model().")
    return joblib.load(MODEL_PATH)


model = None


def get_model():
    global model
    if model is None:
        model = load_model()
    return model


# --- PREDICT FOR SCRAPED TEXT ---
def predict_text(text: str):
    clf = get_model()
    cleaned = clean_text(text)

    proba = clf.predict_proba([cleaned])[0]  # [prob_real, prob_misinfo]
    pred = int(proba[1] >= 0.5)

    # Dictionary containing the prediction, probability of real news, and probability of misinformation
    return {
        "prediction": pred,
        "probability_real": float(proba[0]),
        "probability_misinfo": float(proba[1])
    }
