from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import ride
from flask_app.models.user import User
from flask_app.models.message import Message

@app.route("/rides/post/<int:ride_id>", methods = ['POST'])
def post_message(ride_id):
    if 'user_id' in session:
        data = {
            'message': request.form['message'], 
            'ride_id': ride_id,
            'user_id': session['user_id']
        }
    Message.post_message(data)
    return redirect(f"/rides/{ride_id}")