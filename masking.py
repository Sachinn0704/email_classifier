import re

def mask_pii(text):
    patterns = {
        "full_name": r"\b([A-Z][a-z]+ [A-Z][a-z]+)\b",
        "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
        "phone_number": r"\b\d{10}\b",
        "dob": r"\b\d{2}[/-]\d{2}[/-]\d{4}\b",
        "aadhar_num": r"\b\d{4} \d{4} \d{4}\b",
        "credit_debit_no": r"\b(?:\d[ -]*?){13,16}\b",
        "cvv_no": r"\b\d{3}\b",
        "expiry_no": r"\b(0[1-9]|1[0-2])\/?([0-9]{2})\b"
    }
    entity_list = []
    for entity, pattern in patterns.items():
        for match in re.finditer(pattern, text):
            start, end = match.span()
            original = match.group()
            text = text[:start] + f"[{entity}]" + text[end:]
            entity_list.append({
                "position": [start, start + len(f"[{entity}]")],
                "classification": entity,
                "entity": original
            })
    entity_list.sort(key=lambda x: x["position"][0])
    return text, entity_list

def restore_pii(masked_text, entity_list):
    for entity in reversed(entity_list):
        start, end = entity["position"]
        masked_text = masked_text[:start] + entity["entity"] + masked_text[end:]
    return masked_text
