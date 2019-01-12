from os import urandom
from flask import Flask, render_template, request, session, redirect, url_for, flash
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
    return render_template("index.html")


@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register",methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        success, message = authenticate.register_user(
                request.form['username'],
                request.form['password'],
                request.form['passwordConfirmation'])
        if success:
            flash(message, "success")
            return redirect(url_for('login'))
        else:
            flash(message, "danger")
            return redirect(url_for('register'))


if __name__ == "__main__":
    socketio.run(app, debug=True)
