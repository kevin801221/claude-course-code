def send_notification(ticket):
    return {"recipient": ticket["email"], "status": "queued"}
