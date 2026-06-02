from flask import Flask
from flask_socketio import SocketIO, emit
from routes import register_routes
from userAuth import register_user, login_user

app = Flask(__name__, template_folder='templates', static_folder='public')
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
socketio = SocketIO(app, cors_allowed_origins="*")
register_routes(app)

@socketio.on("register")
def handle_register(data):
    username = data.get("username")
    password = data.get("password")
    result = register_user(username, password)
    emit("register_response", result)

@socketio.on("login")
def handle_login(data):
    username = data.get("username")
    password = data.get("password")
    result = login_user(username, password)
    # Add username to response so client can store it
    if "username" not in result:
        result["username"] = username
    emit("login_response", result)

@socketio.on("message")
def handle_message(data):
    emit("message", data, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, debug=True, host='127.0.0.1', port=5000)
