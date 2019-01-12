from os import urandom
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config["SECRET_KEY"] = urandom(64)
socketio = SocketIO(app)


def message_received(methods=["GET", "POST"]):
    print("message was received!!!")


@socketio.on("my event")
def handle_my_custom_event(json, methods=["GET", "POST"]):
    print("received my event: " + str(json))
    socketio.emit("my response", json, callback=message_received)


@app.route("/")
def index():
    return render_template("index.html", title="Welcome")


@app.route("/chat")
def chat():
    return render_template("chat.html", title="Chatting")


if __name__ == "__main__":
    socketio.run(app, debug=True)
