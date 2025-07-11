from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import mariadb
import sys
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Item
from flask_mail import Mail, Message
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Geheimer Schlüssel für Session-Sicherheit

# SQLAlchemy Konfiguration
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://admin:Webtechnologien123_@webtechnologien-dhsh.ch5e7fok1mgo.eu-central-1.rds.amazonaws.com:3306/webtechnologien"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)  # Initialisiert die DB-Verbindung

@app.route("/")
def index():
    user = session.get("user")  # Holt eingeloggten Benutzer aus der Session
    return render_template("index.html", user=user)  # Startseite

# Produktübersicht
@app.route("/produkte")
def produkte():
    items = Item.query.filter_by(display_online=True).all()  # Nur sichtbare Produkte anzeigen
    return render_template("devices.html", items=items)

# Detailansicht eines Produkts
@app.route("/produkt/<int:item_id>")
def produkt_detail(item_id):
    item = Item.query.get_or_404(item_id)  # Holt das Produkt oder zeigt 404
    return render_template("device_detail.html", item=item)

# Produkt zum Warenkorb hinzufügen
@app.route("/add_to_cart/<int:item_id>", methods=["POST"])
def add_to_cart(item_id):
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")

    if "cart" not in session:
        session["cart"] = []  # Initialisiere Warenkorb, falls noch nicht vorhanden

    cart = session["cart"]
    cart.append({"item_id": item_id, "start_date": start_date, "end_date": end_date})
    session["cart"] = cart  # Aktualisiere Session

    flash("✅ Produkt wurde dem Warenkorb hinzugefügt.")  # Benutzer-Feedback
    return redirect(url_for("warenkorb"))

# Warenkorb anzeigen
@app.route("/warenkorb")
def warenkorb():
    cart = session.get("cart", [])
    items = []
    for entry in cart:
        item = Item.query.get(entry["item_id"])
        if item:
            start_date_obj = datetime.strptime(entry["start_date"], "%Y-%m-%d")
            end_date_obj = datetime.strptime(entry["end_date"], "%Y-%m-%d")
            days = (end_date_obj - start_date_obj).days
            items.append({
                "item": item,
                "start_date": start_date_obj,
                "end_date": end_date_obj,
                "days": days
            })
    return render_template("warenkorb.html", items=items)

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            conn = mariadb.connect(
                host="webtechnologien-dhsh.ch5e7fok1mgo.eu-central-1.rds.amazonaws.com",
                port=3306,
                user="admin",
                password="Webtechnologien123_",
                database="webtechnologien"
            )
            cur = conn.cursor()
            cur.execute("SELECT name, password FROM users WHERE email=?", (email,))
            user = cur.fetchone()
            conn.close()

            if user and check_password_hash(user[1], password):
                session["user"] = email  # Login erfolgreich, speichert E-Mail in Session
                flash(f"✅ Willkommen zurück, {user[0]}!")
                return redirect(url_for("index"))
            else:
                flash("❌ Login fehlgeschlagen – falsche Daten")

        except mariadb.Error as e:
            flash(f"❌ Fehler bei der DB-Anfrage: {e}")

        return redirect(url_for("login"))

    return render_template("login.html")

# Registrierung
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        hashed_password = generate_password_hash(password)

        try:
            conn = mariadb.connect(
                host="webtechnologien-dhsh.ch5e7fok1mgo.eu-central-1.rds.amazonaws.com",
                port=3306,
                user="admin",
                password="Webtechnologien123_",
                database="webtechnologien"
            )
            cur = conn.cursor()
            cur.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                        (name, email, hashed_password))
            conn.commit()
            conn.close()

            flash("✅ Registrierung erfolgreich – bitte einloggen.")
            return redirect(url_for("login"))

        except mariadb.Error as e:
            flash(f"❌ Fehler bei der Registrierung: {e}")
            return redirect(url_for("register"))

    return render_template("register.html")

# Logout
@app.route("/logout")
def logout():
    session.clear()  # Löscht alle Daten aus der Session
    flash("✅ Du wurdest erfolgreich ausgeloggt.")
    return redirect(url_for("index"))

# Checkout-Route (nicht mehr aktiv genutzt, Ersatz: /anfrage-absenden)
@app.route("/checkout")
def checkout():
    items = session.get("cart", [])
    if not items:
        flash("Dein Warenkorb ist leer.")
        return redirect(url_for("produkte"))

    flash("✅ Deine Anfrage wurde erfolgreich übermittelt!")
    session["cart"] = []  # Leert den Warenkorb
    return redirect(url_for("index"))

# Mail-Konfiguration (z. B. für GMX)
app.config['MAIL_SERVER'] = 'mail.gmx.net'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'webtech1@gmx.de'
app.config['MAIL_PASSWORD'] = '2KIPBLCWVX3E4ABYBMP6'
app.config['MAIL_DEFAULT_SENDER'] = 'webtech1@gmx.de'

mail = Mail(app)  # Initialisiere Flask-Mail mit der App

# Anfrage per Mail versenden
@app.route("/anfrage-absenden", methods=["POST"])
def anfrage_absenden():
    cart = session.get("cart", [])
    if not cart:
        flash("❌ Dein Warenkorb ist leer.")
        return redirect(url_for("warenkorb"))

    items = []
    for entry in cart:
        item = Item.query.get(entry["item_id"])
        if item:
            try:
                start = datetime.strptime(entry["start_date"], "%Y-%m-%d")
                end = datetime.strptime(entry["end_date"], "%Y-%m-%d")
            except ValueError:
                continue

            items.append({
                "name": item.name,
                "start_date": start.strftime('%d.%m.%Y'),
                "end_date": end.strftime('%d.%m.%Y'),
                "price": item.price_per_day
            })

    # E-Mail-Versand mit gerendertem Texttemplate
    try:
        empfaenger = "allmail@posteo.de"  # Zieladresse für Test/Support
        inhalt = render_template("email_template.txt", items=items)
        msg = Message("Neue Anfrage von der Website",
                      sender=app.config["MAIL_USERNAME"],
                      recipients=[empfaenger],
                      body=inhalt)
        mail.send(msg)
        flash("✅ Deine Anfrage wurde erfolgreich versendet!")
    except Exception as e:
        flash(f"❌ Fehler beim Senden der E-Mail: {e}")

    return redirect(url_for("index"))

# Start der Anwendung + Test der Datenbankverbindung
if __name__ == "__main__":
    try:
        conn = mariadb.connect(
            host="webtechnologien-dhsh.ch5e7fok1mgo.eu-central-1.rds.amazonaws.com",
            port=3306,
            user="admin",
            password="Webtechnologien123_",
            database="webtechnologien"
        )
        cur = conn.cursor()
        cur.execute("SELECT 'DB-Verbindung OK'")
        result = cur.fetchone()
        conn.close()
        print(f"[Startup] DB-Verbindung erfolgreich: {result[0]}")
    except mariadb.Error as e:
        print(f"[Startup] Fehler bei der DB-Verbindung: {e}")
        sys.exit(1)

    app.run(debug=True)  # Startet die Flask-App im Debug-Modus
