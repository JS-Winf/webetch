from flask_mail import Mail, Message  # Importiert die Mail-Komponenten von Flask

mail = Mail()  # Initialisiert das Mail-Objekt (wird später mit Flask-App konfiguriert)

def send_request_email(app, recipient, cart_items):
    # Funktion zum Versenden einer Anfrage-E-Mail mit ausgewählten Warenkorbinhalten
    # Parameter:
    # - app: die aktuelle Flask-App (für Kontextzugriff)
    # - recipient: E-Mail-Adresse des Empfängers
    # - cart_items: Liste der angefragten Produkte (mit Namen, Zeitraum, Preis)

    with app.app_context():  # Stellt sicher, dass innerhalb des App-Kontexts gearbeitet wird
        subject = "Neue Produktanfrage"  # Betreff der E-Mail
        sender = app.config["MAIL_USERNAME"]  # Absenderadresse aus App-Konfiguration

        message_body = "Hallo,\n\nfolgende Anfrage wurde gestellt:\n\n"  # Einleitungstext

        for item in cart_items:
            # Fügt für jeden Artikel eine Zeile mit Name, Zeitraum und Preis hinzu
            message_body += f"- {item['name']} (von {item['from_date']} bis {item['to_date']}, {item['price_per_day']} €/Tag)\n"

        message_body += "\nViele Grüße,\nIhr Eventverleih"  # Abschlusstext

        msg = Message(
            subject=subject,
            sender=sender,
            recipients=[recipient],  # Zieladresse(n) als Liste
            body=message_body  # Textinhalt der E-Mail
        )

        mail.send(msg)  # Versendet die E-Mail über den konfigurierten Mailserver
