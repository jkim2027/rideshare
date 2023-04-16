from flask_app import app
from flask_app.controllers import user_controller, ride_controller, index_controller, message_controller

app.secret_key = 'practice makes perfect'


if __name__ == "__main__":
    app.run(debug = True, port = 5001)