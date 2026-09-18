from fastapi import FastAPI
from pydantic import BaseModel, Field
from masking import mask_pii, restore_pii
from classification import classify_email_with_confidence

app = FastAPI()


class EmailRequest(BaseModel):
    input_email_body: str = Field(..., min_length=1, description="Email body to classify")


@app.post("/classify")
async def classify(request: EmailRequest):
    email = request.input_email_body
    masked_email, entity_list = mask_pii(email)
    category, confidence = classify_email_with_confidence(masked_email)
    original_email = restore_pii(masked_email, entity_list)

    return {
        "input_email_body": original_email,
        "list_of_masked_entities": entity_list,
        "masked_email": masked_email,
        "category_of_the_email": category,
        "classification_confidence": confidence,
    }
