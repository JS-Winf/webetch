#Einstiegspunkt
from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = os.random(24) # Sessions für zb. Login

@app.route("/")
def index():
    return render_template("index.html") #Startseite

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        #Hier später Login Logik
        return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def regiser():
    if request.method == "POST":
        # Hier später Registrierung
        return redirect(url_for("login"))
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)
    