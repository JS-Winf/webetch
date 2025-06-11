from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import mariadb
import sys
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
def index():
    user = session.get("user")
    return render_template("index.html", user=user)

@app.route("/produkte")
def produkte():
    return render_template("device_detail.html")

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
 #Teste DB-Verbindung beim Start
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
        print(f" [Startup] DB-Verbindung erfolgreich: {result[0]}")
    except mariadb.Error as e:
        print(f" [Startup] Fehler bei der DB-Verbindung: {e}")
        sys.exit(1)                                                 #Bei Fehler App nicht starten

    # Flask-App starten
    app.run(debug=True)
