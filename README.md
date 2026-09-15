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

## Key Learning Outcomes

- Text preprocessing and PII protection
- Supervised machine-learning workflow
- Confidence-aware classification
- Model serialization with Joblib
- REST API development with FastAPI
- Separating preprocessing, inference, and serving logic

## Future Improvements

- Add automated tests
- Add structured logging without exposing PII
- Expand the training dataset and evaluation metrics
- Add authentication and rate limiting to the API
- Containerize the service for deployment
