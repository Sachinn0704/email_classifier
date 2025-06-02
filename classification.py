import joblib
import re

model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

def preprocess(text):
    text = re.sub(r"[^\w\s]", "", text)
    return text.lower()

def classify_email(text):
    text = preprocess(text)
    X = vectorizer.transform([text])
    prediction = model.predict(X)[0]
    return prediction
