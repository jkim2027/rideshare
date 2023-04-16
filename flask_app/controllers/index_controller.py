from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import render_template, redirect, session

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")