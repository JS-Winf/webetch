from flask_mail import Mail, Message

mail = Mail()

def send_request_email(app, recipient, cart_items):
    with app.app_context():
        subject = "Neue Produktanfrage"
        sender = app.config["MAIL_USERNAME"]

        message_body = "Hallo,\n\nfolgende Anfrage wurde gestellt:\n\n"

        for item in cart_items:
            message_body += f"- {item['name']} (von {item['from_date']} bis {item['to_date']}, {item['price_per_day']} €/Tag)\n"

        message_body += "\nBitte melden Sie sich beim Kunden zurück.\nViele Grüße,\nIhr Eventverleih"

        msg = Message(subject=subject, sender=sender, recipients=[recipient], body=message_body)
        mail.send(msg)
