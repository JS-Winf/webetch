from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import mariadb
import sys
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Item

app = Flask(__name__)
app.secret_key = os.urandom(24)

# SQLAlchemy konfigurieren
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://admin:Webtechnologien123_@webtechnologien-dhsh.ch5e7fok1mgo.eu-central-1.rds.amazonaws.com:3306/webtechnologien"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route("/")
def index():
    user = session.get("user")
    return render_template("index.html", user=user)

@app.route("/produkte")
def produkte():
    items = Item.query.filter_by(display_online=True).all()
    return render_template("devices.html", items=items)

@app.route("/produkt/<int:item_id>")
def produkt_detail(item_id):
    item = Item.query.get_or_404(item_id)
    return render_template("device_detail.html", item=item)

@app.route("/add-to-cart/<int:item_id>", methods=["POST"])
def add_to_cart(item_id):
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")

    cart = session.get("cart", [])
    cart.append({
        "item_id": item_id,
        "start_date": start_date,
        "end_date": end_date
    })
    session["cart"] = cart

    flash("✅ Produkt wurde zum Warenkorb hinzugefügt.")
    return redirect(url_for("warenkorb"))

@app.route("/warenkorb")
def warenkorb():
    cart = session.get("cart", [])
    items = []
    for entry in cart:
        item = Item.query.get(entry["item_id"])
        if item:
            items.append({
                "item": item,
                "start_date": entry["start_date"],
                "end_date": entry["end_date"]
            })
    return render_template("warenkorb.html", items=items)

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
                session["user"] = email
                flash(f"✅ Willkommen zurück, {user[0]}!")
                return redirect(url_for("index"))
            else:
                flash("❌ Login fehlgeschlagen – falsche Daten")

        except mariadb.Error as e:
            flash(f"❌ Fehler bei der DB-Anfrage: {e}")

        return redirect(url_for("login"))

    return render_template("login.html")

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

@app.route("/logout")
def logout():
    session.clear()
    flash("✅ Du wurdest erfolgreich ausgeloggt.")
    return redirect(url_for("index"))

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

    app.run(debug=True)
