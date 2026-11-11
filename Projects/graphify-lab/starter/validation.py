def validate_ticket(title, email):
    if not title.strip():
        raise ValueError("title is required")
    if "@" not in email:
        raise ValueError("invalid email")
