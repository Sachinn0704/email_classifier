from fastapi import FastAPI, Request
from pydantic import BaseModel
from masking import mask_pii, restore_pii
from classification import classify_email

app = FastAPI()

class EmailRequest(BaseModel):
    input_email_body: str

@app.post("/classify")
async def classify(request: EmailRequest):
    email = request.input_email_body
    masked_email, entity_list = mask_pii(email)
    category = classify_email(masked_email)
    original_email = restore_pii(masked_email, entity_list)
    return {
        "input_email_body": original_email,
        "list_of_masked_entities": entity_list,
        "masked_email": masked_email,
        "category_of_the_email": category
    }
