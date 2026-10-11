import re


PATTERNS = {
    "full_name": r"\b([A-Z][a-z]+ [A-Z][a-z]+)\b",
    "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "phone_number": r"\b\d{10}\b",
    "dob": r"\b\d{2}[/-]\d{2}[/-]\d{4}\b",
    "aadhar_num": r"\b\d{4} \d{4} \d{4}\b",
    "credit_debit_no": r"\b(?:\d[ -]*?){13,16}\b",
    "cvv_no": r"\b\d{3}\b",
    "expiry_no": r"\b(0[1-9]|1[0-2])\/?([0-9]{2})\b",
}


def mask_pii(text):
    """Mask detected PII while preserving reversible placeholder positions.

    Matches are found against the original text, then applied left-to-right.
    This avoids corrupting offsets when replacements change the string length.
    Overlapping matches are resolved by keeping the longest match at a given
    start position, preventing a card number from also being masked as a CVV.
    """
    if not isinstance(text, str):
        raise TypeError("Text to mask must be a string")

    matches = []
    for entity, pattern in PATTERNS.items():
        for match in re.finditer(pattern, text):
            start, end = match.span()
            matches.append((start, end, entity, match.group()))

    # Earlier starts win; for overlapping candidates, prefer the longer span.
    matches.sort(key=lambda item: (item[0], -(item[1] - item[0])))
    selected = []
    cursor = 0
    for start, end, entity, original in matches:
        if start < cursor:
            continue
        selected.append((start, end, entity, original))
        cursor = end

    masked_parts = []
    entity_list = []
    source_cursor = 0
    masked_length = 0
    for start, end, entity, original in selected:
        unchanged = text[source_cursor:start]
        masked_parts.append(unchanged)
        masked_length += len(unchanged)

        placeholder = f"[{entity}]"
        placeholder_start = masked_length
        masked_parts.append(placeholder)
        masked_length += len(placeholder)
        entity_list.append({
            "position": [placeholder_start, masked_length],
            "classification": entity,
            "entity": original,
        })
        source_cursor = end

    masked_parts.append(text[source_cursor:])
    return "".join(masked_parts), entity_list


def restore_pii(masked_text, entity_list):
    """Restore placeholders produced by mask_pii, from right to left."""
    for entity in sorted(entity_list, key=lambda item: item["position"][0], reverse=True):
        start, end = entity["position"]
        masked_text = masked_text[:start] + entity["entity"] + masked_text[end:]
    return masked_text
