from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import ride
from flask_app.models.user import User
from flask_app.models.message import Message

@app.route("/rides/new")
def new_ride():
    if 'user_id' in session:
        data = {'id': session['user_id']}
        user = User.get_by_id(data)
    return render_template("ride/new_ride.html", user = user)

@app.route("/rides/new", methods = ['POST'])
def request_ride():
    if not ride.Ride.validate_ride(request.form):
        return redirect("/rides/new")
    data = {
        'user_id': session['user_id'],
        'destination': request.form['destination'],
        'pickup': request.form['pickup'],
        'ride_date': request.form['ride_date'],
        'details': request.form['details'],
        'driver_id': None
    }
    ride.Ride.new_ride(data)
    return redirect("/rides/dashboard")

@app.route("/rides/delete/<int:ride_id>")
def delete_ride(ride_id):
    ride.Ride.delete_ride(ride_id)
    return redirect("/rides/dashboard")

@app.route("/rides/<int:ride_id>")
def show_one(ride_id):
    data = {'id': session['user_id']}
    user = User.get_by_id(data)
    one_ride = ride.Ride.get_one_ride(ride_id)
    message = Message.get_messages(ride_id)
    return render_template("ride/ride_detail.html", one_ride=one_ride, user=user, all_message=message)

@app.route("/rides/edit/<int:ride_id>")
def edit_ride(ride_id):
    one_ride = ride.Ride.get_one_ride(ride_id)
    return render_template("ride/edit_ride.html", ride=one_ride)

@app.route("/rides/edit/<int:ride_id>", methods = ['POST'])
def update_ride(ride_id):
    if not ride.Ride.validate_update(request.form):
        return redirect(f"/rides/edit/{ride_id}")
    data = {
        'pickup': request.form['pickup'],
        'details': request.form['details'],
        'ride_id': ride_id
    }
    ride.Ride.update_ride(data)
    return redirect(f"/rides/{ride_id}")