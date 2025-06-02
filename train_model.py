import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

df = pd.read_csv("data/support_emails.csv")
X = df["email"]
y = df["category"]

vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

model = MultinomialNB()
model.fit(X_vec, y)

joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
