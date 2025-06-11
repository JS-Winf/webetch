# models.py – Datenbankmodelle: User, Item (Gerät)

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'  # explizit setzen, falls DB-Tabelle klein geschrieben ist

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


class Item(db.Model):
    __tablename__ = 'Items'  # exakt so wie in der bestehenden Datenbank!

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100))
    description = db.Column(db.Text)
    price_per_day = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    image_url = db.Column(db.String(255))
    is_variation_visible = db.Column(db.Boolean)
    display_online = db.Column(db.Boolean)
    tax_rate = db.Column(db.Float)
