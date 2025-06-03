#Einstiegspunkt
from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from flask import g

app = Flask(__name__)
app.secret_key = os.urandom(24) # Sessions für zb. Login

@app.route("/")
def index():
    user = session.get("user")
    return render_template("index.html", user=user) #Startseite

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        #Hier später Login Logik
        email = request.form.get("email")
        password = request.form.get("password")

        # Beispielwerte
        if email == "test@event.de" and password == "1234":
            session["user"] = email
            flash("Login erfolgreich")
            return redirect(url_for("index"))
        else:
            flash("Login fehlgeschlagen")

        return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        # Hier später Registrierung
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        # Hier validieren oder speichern
        flash(f"Registrierung erfolgreich für {name} ({email})")
        return redirect(url_for("login"))
    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
