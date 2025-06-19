# models.py – Datenbankmodelle: User, Item etc.

from flask_sqlalchemy import SQLAlchemy  # Importiert SQLAlchemy für ORM-Funktionalität

db = SQLAlchemy()  # Erstellt eine SQLAlchemy-Instanz, wird später mit Flask-App verknüpft

# Modell für Benutzer (entspricht der Tabelle 'users')
class User(db.Model):
    __tablename__ = 'users'  # Tabellenname in der Datenbank

    id = db.Column(db.Integer, primary_key=True)  # Primärschlüssel (automatisch hochzählend)
    name = db.Column(db.String(100), nullable=False)  # Name des Benutzers (Pflichtfeld)
    email = db.Column(db.String(120), unique=True, nullable=False)  # E-Mail-Adresse (einmalig & Pflichtfeld)
    password = db.Column(db.String(200), nullable=False)  # Passwort (verschlüsselt gespeichert)

# Modell für Produkte (entspricht der Tabelle 'Items')
class Item(db.Model):
    __tablename__ = 'Items'  # Tabellenname exakt wie in der bestehenden DB angegeben (Groß-/Kleinschreibung beachten)

    id = db.Column(db.Integer, primary_key=True)  # Primärschlüssel
    name = db.Column(db.String(100), nullable=False)  # Produktname (Pflichtfeld)
    category = db.Column(db.String(100))  # Produktkategorie
    description = db.Column(db.Text)  # Beschreibungstext (beliebig lang)
    price_per_day = db.Column(db.Float)  # Mietpreis pro Tag
    quantity = db.Column(db.Integer)  # Anzahl verfügbarer Artikel
    image_url = db.Column(db.String(255))  # URL zum Produktbild
    is_variation_visible = db.Column(db.Boolean)  # Sichtbarkeit für Varianten (z. B. Farben, Größen)
    display_online = db.Column(db.Boolean)  # Flag zur Online-Anzeige im Shop
    tax_rate = db.Column(db.Float)  # Mehrwertsteuersatz in Prozent
