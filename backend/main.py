from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import mariadb
import sys

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
def index():
    user = session.get("user")
    return render_template("index.html", user=user)

@app.route("/login", methods=["GET", "POST"])                     #Login
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email == "test@event.de" and password == "1234":
            session["user"] = email
            flash("Login erfolgreich")
            return redirect(url_for("index"))
        else:
            flash("Login fehlgeschlagen")
        return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])                 #Registrierung
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        flash(f"Registrierung erfolgreich für {name} ({email})")
        return redirect(url_for("login"))
    return render_template("register.html")

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
