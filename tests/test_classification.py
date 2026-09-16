import unittest
from unittest.mock import patch

import classification


class FakeVectorizer:
    def transform(self, texts):
        self.last_texts = texts
        return texts


class FakeModel:
    def predict(self, features):
        return ["Request"]

    def predict_proba(self, features):
        return [[0.05, 0.90, 0.05]]


class ClassificationTests(unittest.TestCase):
    def test_preprocess_normalizes_text(self):
        self.assertEqual(
            classification.preprocess("  Password RESET!!! "),
            "password reset",
        )

    def test_preprocess_rejects_non_string_input(self):
        with self.assertRaises(TypeError):
            classification.preprocess(None)

    def test_missing_model_artifacts_raise_clear_error(self):
        with patch.object(classification, "_MODEL", None), patch.object(
            classification, "_VECTORIZER", None
        ), patch.object(classification.Path, "exists", return_value=False):
            with self.assertRaisesRegex(FileNotFoundError, "Missing trained artifacts"):
                classification.classify_email("Please reset my password")

    def test_classification_returns_category_and_confidence(self):
        fake_model = FakeModel()
        fake_vectorizer = FakeVectorizer()
        with patch.object(classification, "_MODEL", fake_model), patch.object(
            classification, "_VECTORIZER", fake_vectorizer
        ):
            category, confidence = classification.classify_email_with_confidence(
                "Please reset my password!"
            )

        self.assertEqual(category, "Request")
        self.assertEqual(confidence, 0.90)
        self.assertEqual(fake_vectorizer.last_texts, ["please reset my password"])


if __name__ == "__main__":
    unittest.main()
