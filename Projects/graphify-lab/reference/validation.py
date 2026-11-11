def validate_ticket(title, email):
    if not title.strip():
        raise ValueError("title is required")
    recipient = email.strip() if email is not None else ""
    if not recipient:
        return None
    if "@" not in recipient:
        raise ValueError("invalid email")
    return recipient
