from os import urandom
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_socketio import SocketIO
from urllib.parse import urlencode
import sqlite3
import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
from utils import authenticate

app = Flask(__name__)
app.config["SECRET_KEY"] = urandom(64)
socketio = SocketIO(app)

DB_FILE = "cyber.db"


@socketio.on("user connected")
def handle_user_connected(json, methods=["GET", "POST"]):
    command = f"UPDATE profiles SET ActiveSession = {request.sid} WHERE UserID == {session['uid']}"
    db = sqlite3.connect(DB_FILE, check_same_thread=False)  # open if file exists, otherwise create
    c = db.cursor()
    c.execute(command)
    db.commit()
    db.close()


@socketio.on("disconnect")
def handle_disconnect(json, methods=["GET", "POST"]):
    command = f"UPDATE profiles SET ActiveSession = 0 WHERE UserID == {session['uid']}"
    db = sqlite3.connect(DB_FILE, check_same_thread=False)  # open if file exists, otherwise create
    c = db.cursor()
    c.execute(command)
    db.commit()
    db.close()


@socketio.on("user sent message")
def handle_user_sent_message(json, methods=["GET", "POST"]):
    command = f"INSERT INTO messages ('FromUserID', 'ToUserID', 'Message', 'Flagged') VALUES ({session['uid']}, {json['touid']}, {json['data']}, {toFlag(json['data'])})"
    db = sqlite3.connect(DB_FILE, check_same_thread=False)  # open if file exists, otherwise create
    c = db.cursor()
    c.execute(command)
    db.commit()
    db.close()


def get_cyberbullied(content):
    '''Returns api dict based on user msg'''
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '7eb4070eb5a7451d8d99d6767263a0d0',
    }

    params = urllib.parse.urlencode({})

    try:
        conn = http.client.HTTPSConnection('api.tisane.ai')
        body = '{"language":"en", "content":' + '"' + content + '",' + '"settings":{}}'
        print("This is the body", body)
        conn.request("POST", "/parse?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        dict = json.loads(data.decode('utf-8'))
        print(dict)
        return dict
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


# get_cyberbullied("You are an idiot.")


def toFlag(content):
    data = get_cyberbullied(content)
    if (data['sentiment_expressions'][0]['polarity'] == 'negative' and (
            data['abuse'][0]['severity'] == "medium" or data['abuse'][0]['severity'] == "high" or data['abuse'][0][
        'severity'] == "extreme")):
        print("You are getting flagged")
        return True
    return False


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat")
def chat():
    return render_template("chat.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        username = authenticate.is_loggedin(session)
        if username:
            flash("You are already logged in!", "warning")
            return redirect(url_for('login'))
        else:
            return render_template("login.html")

        print("IS IT A SUCCESS",success)
    else:
        success, message, uid = authenticate.login_user(
            request.form['username'],
            request.form['password'])
        if success:
            flash(message, "success")
            session['loggedin'] = request.form['username']
            session['uid'] = uid
            return redirect(url_for('chat', username=request.form['username']))
        else:
            flash(message, "danger")
            return redirect(url_for('login'))


@app.route("/register", methods=["GET", "POST"])
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

@app.route('/logout', methods=["GET", "POST"])
def logout():
    '''Handles logging out of user account'''

    if authenticate.is_loggedin(session):
        print(session)
        session.pop('loggedin', None)
        session.pop('uid', None)
        print(session)
        flash("Successfully logged out.", "success")
    else:
        flash("You are not logged in!", "danger")
    return redirect(url_for('login'))
if __name__ == "__main__":
    socketio.run(app, debug=True)
