import joblib
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
_MODEL = None
_VECTORIZER = None


def _load_artifacts():
    """Load the trained model artifacts only when classification is requested."""
    global _MODEL, _VECTORIZER

    if _MODEL is None or _VECTORIZER is None:
        model_path = BASE_DIR / "model.pkl"
        vectorizer_path = BASE_DIR / "vectorizer.pkl"
        missing = [path.name for path in (model_path, vectorizer_path) if not path.exists()]
        if missing:
            raise FileNotFoundError(
                "Missing trained artifacts: " + ", ".join(missing) + ". "
                "Run train_model.py before classifying emails."
            )
        _MODEL = joblib.load(model_path)
        _VECTORIZER = joblib.load(vectorizer_path)

    return _MODEL, _VECTORIZER


def preprocess(text):
    """Normalize an email body into the format expected by the TF-IDF vectorizer."""
    if not isinstance(text, str):
        raise TypeError("Email text must be a string")
    text = re.sub(r"[^\w\s]", "", text)
    return text.lower().strip()


def classify_email(text):
    """Return the predicted category for an email."""
    model, vectorizer = _load_artifacts()
    cleaned_text = preprocess(text)
    X = vectorizer.transform([cleaned_text])
    return model.predict(X)[0]


def classify_email_with_confidence(text):
    """Return the predicted category and highest class probability."""
    model, vectorizer = _load_artifacts()
    cleaned_text = preprocess(text)
    X = vectorizer.transform([cleaned_text])
    prediction = model.predict(X)[0]

    if not hasattr(model, "predict_proba"):
        return prediction, None

    probabilities = model.predict_proba(X)[0]
    return prediction, float(max(probabilities))
