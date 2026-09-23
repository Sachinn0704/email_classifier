import unittest
from unittest.mock import patch

import classification


class FakeVectorizer:
    def transform(self, texts):
        self.last_text = texts[0]
        return texts


class FakeModel:
    def predict(self, X):
        return ["support"]

    def predict_proba(self, X):
        return [[0.15, 0.85]]


class PredictionOnlyModel:
    def predict(self, X):
        return ["request"]


class ClassificationTests(unittest.TestCase):
    def setUp(self):
        classification._MODEL = FakeModel()
        classification._VECTORIZER = FakeVectorizer()

    def tearDown(self):
        classification._MODEL = None
        classification._VECTORIZER = None

    def test_preprocess_normalizes_text(self):
        self.assertEqual(
            classification.preprocess("  Urgent! HELP@example.com... "),
            "urgent help examplecom",
        )

    def test_preprocess_rejects_non_string_input(self):
        with self.assertRaises(TypeError):
            classification.preprocess(None)

    def test_classify_email_returns_prediction(self):
        result = classification.classify_email("Need help with my account!")
        self.assertEqual(result, "support")

    def test_classify_email_with_confidence(self):
        label, confidence = classification.classify_email_with_confidence("Need help")
        self.assertEqual(label, "support")
        self.assertAlmostEqual(confidence, 0.85)

    def test_confidence_is_optional_for_prediction_only_models(self):
        classification._MODEL = PredictionOnlyModel()
        label, confidence = classification.classify_email_with_confidence("Please update my access")
        self.assertEqual(label, "request")
        self.assertIsNone(confidence)

    @patch.object(classification.Path, "exists", return_value=False)
    def test_missing_artifacts_raise_clear_error(self, _exists):
        classification._MODEL = None
        classification._VECTORIZER = None
        with self.assertRaisesRegex(FileNotFoundError, "Run train_model.py"):
            classification.classify_email("Hello")


if __name__ == "__main__":
    unittest.main()
