from validation import validate_ticket
from repository import save_ticket
from notification import send_notification


def create_ticket(title, email):
    recipient = validate_ticket(title, email)
    ticket = save_ticket(title, recipient)
    if recipient is not None:
        send_notification(ticket)
    return ticket
