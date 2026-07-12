# Email Classifier

A machine learning system that classifies support emails into predefined categories, with built-in PII (Personally Identifiable Information) masking to protect sensitive data before processing.

## Overview

This project automatically categorizes incoming support emails (e.g., Billing, Technical Issue, Account Request, General Inquiry) using a trained machine learning model. Before classification, any personal information present in the email — such as names, email addresses, and phone numbers — is masked to ensure sensitive data is not exposed during processing or logging.

## Features

- **PII Masking** — Automatically detects and masks sensitive information (names, emails, phone numbers, etc.) from email text before classification.
- **ML-based Classification** — Uses a trained model to predict the correct category for a given email.
- **REST API** — Exposes an endpoint to classify new emails on demand.
- **Model Training Pipeline** — Includes a script to train the classifier on your own labeled dataset.

## Project Structure

```
email_classifier/
├── app.py               # Entry point — runs the API/service
├── classification.py    # Core logic for classifying emails using the trained model
├── masking.py           # PII detection and masking logic
├── train_model.py       # Script to train and save the ML model
├── requirements.txt     # Python dependencies
└── README.md
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Sachinn0704/email_classifier.git
   cd email_classifier
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. Train the model
Train the classifier on your dataset:
```bash
python train_model.py
```
This will process the training data and save the trained model for later use in classification.

### 2. Run the application
Start the app to classify emails:
```bash
python app.py
```

### 3. Classify an email
Send an email's text to the classification endpoint (adjust based on your actual API route):
```bash
curl -X POST http://localhost:5000/classify \
  -H "Content-Type: application/json" \
  -d '{"email_text": "Hi, I was charged twice for my last invoice."}'
```

Example response:
```json
{
  "masked_text": "Hi, I was charged twice for my last invoice.",
  "predicted_category": "Billing Issue"
}
```

## How It Works

1. **Input** — A raw email (subject + body) is received.
2. **Masking** — `masking.py` scans the text and replaces any PII (names, emails, phone numbers) with placeholder tokens.
3. **Classification** — `classification.py` loads the trained model and predicts the most likely category for the masked email.
4. **Output** — The predicted category (and optionally the masked text) is returned to the caller.

## Tech Stack

- **Python**
- **Scikit-learn** (or specify your actual ML library) for model training and inference
- **Flask** (or specify your actual framework) for the API layer
- **Regex / NLP libraries** for PII detection

## Future Improvements

- Add support for more PII types (addresses, IDs, etc.)
- Improve classification accuracy with a larger labeled dataset
- Add unit tests and CI/CD pipeline
- Containerize with Docker for easier deployment

## License

This project is open source. Feel free to use and modify it.

## Author

**Sachin** — [GitHub](https://github.com/Sachinn0704)
