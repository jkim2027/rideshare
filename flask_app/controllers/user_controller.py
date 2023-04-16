from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, ride


@app.route("/rides/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect("/")
    else:
        data = {'id': session['user_id']}
        one_user = user.User.get_by_id(data)
        all_rides = ride.Ride.get_all()
    return render_template("dashboard.html", one_user = one_user, all_rides=all_rides)

@app.route("/register", methods = ['POST'])
def register():
    if not user.User.validate_user(request.form):
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }
    user_id = user.User.register_user(data)
    session['user_id'] = user_id
    return redirect("/rides/dashboard")

@app.route("/login", methods = ['POST'])
def login():
    data = {'email': request.form['email']}
    user_in_db = user.User.get_by_email(data)
    if len(request.form['email']) <= 0 and len(request.form['password']) <= 0:
        flash("All fields required.", 'login')
        return redirect("/")
    if not user_in_db:
        flash("Invalid email address.", 'login')
        return redirect ("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid password.", 'login')
        return redirect("/")
    session['user_id'] = user_in_db.id
    return redirect("/rides/dashboard")

@app.route("/rides/dashboard/<int:ride_id>", methods = ['POST'])
def update_driver_to_rider(ride_id):
    data = {
        'driver_id': session['user_id'],
        'ride_id': ride_id
    }
    user.User.update_driver_to_rider(data)
    return redirect("/rides/dashboard")

@app.route("/rides/dashboard/cancel/<int:ride_id>", methods = ['POST'])
def cancel_ride(ride_id):
    data = {
        'ride_id': ride_id
    }
    user.User.cancel_ride(data)
    return redirect("/rides/dashboard")
