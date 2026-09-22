# Privacy-Aware Email Classification API

A Python machine-learning service that classifies support emails into predefined categories while masking personally identifiable information (PII) before classification and processing.

## Project Summary

The project separates the workflow into PII masking, model inference, model training, and an API layer. It is designed for support-email automation where sensitive information should be removed before text is processed by the classifier.

## Main Features

- PII masking for email text
- Machine-learning based email classification
- Confidence score returned with each prediction
- Model training pipeline
- FastAPI service for classification requests
- JSON API responses

## Privacy and Safety Notes

PII masking happens before the sanitized text is passed to the classifier. The masking layer is intended to protect common identifiers such as names, email addresses, phone numbers, dates of birth, government IDs, and payment-card details.

For production use, the API should be treated as a privacy-sensitive service:

- Do not log raw request bodies or masked/unmasked payloads containing sensitive data.
- Keep model artifacts and training datasets under controlled access.
- Use HTTPS and authentication before exposing the API outside a trusted network.
- Apply rate limiting and request-size limits at the API gateway.
- Review masking rules whenever new PII formats are introduced.
- Treat the classifier confidence as a routing signal, not as proof that a prediction is correct.

The repository focuses on the application-level masking and classification workflow; production deployments should add operational controls appropriate to the environment and applicable privacy requirements.

## Technology Stack

- Python
- FastAPI
- Uvicorn
- Scikit-learn
- Pandas
- Joblib

## Project Structure

```text
.
├── app.py
├── classification.py
├── masking.py
├── train_model.py
├── tests/
│   └── test_classification.py
├── requirements.txt
└── README.md
```

## Workflow

1. Receive email text through the API.
2. Detect sensitive information using the masking module.
3. Replace detected PII with safe placeholder values.
4. Pass the sanitized text to the trained classifier.
5. Return the predicted support category and classification confidence.

## Setup

### 1. Create a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\\Scripts\\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Train the model

```bash
python train_model.py
```

### 4. Start the API

```bash
uvicorn app:app --reload
```

## Testing

The repository includes unit tests for text preprocessing, invalid input handling, missing model artifacts, and confidence-aware classification.

Run the test suite with:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

The tests use lightweight fakes and mocks for model inference, so classification logic can be validated without requiring trained model artifacts.

## API Usage

### `POST /classify`

Request body:

```json
{
  "input_email_body": "Please help me reset my account password."
}
```

Example response shape:

```json
{
  "input_email_body": "Please help me reset my account password.",
  "list_of_masked_entities": [],
  "masked_email": "Please help me reset my account password.",
  "category_of_the_email": "Request",
  "classification_confidence": 0.93
}
```

The confidence value is produced by the classifier and is useful when downstream systems need to distinguish high-confidence predictions from cases that may require human review.

### Quick API check with cURL

After starting the API locally, the endpoint can be exercised without a separate client:

```bash
curl -X POST "http://127.0.0.1:8000/classify" \
  -H "Content-Type: application/json" \
  -d '{"input_email_body":"Please reset my account password."}'
```

For privacy testing, use synthetic addresses, phone numbers, IDs, and other placeholder data rather than real personal information.

## Key Learning Outcomes

- Text preprocessing and PII protection
- Supervised machine-learning workflow
- Confidence-aware classification
- Model serialization with Joblib
- REST API development with FastAPI
- Separating preprocessing, inference, and serving logic
- Unit testing with mocks and deterministic fixtures

## Future Improvements

- Add structured logging without exposing PII
- Expand the training dataset and evaluation metrics
- Add authentication and rate limiting to the API
- Containerize the service for deployment
