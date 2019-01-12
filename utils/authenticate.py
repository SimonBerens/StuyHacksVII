import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def register_user(username, password, repassword):
    '''
    Attempts to register a user and enter it in the users table.
    Returns a tuple containing a boolean indicating success
    and a message to flash to the user.
    '''
    if username == '' or password == '' or repassword == '':
        return (False, "Please fill in all fields.")
    elif password != repassword:
        return (False, "Passwords do not match!")

    with sqlite3.connect("cyber.db") as db:
        c = db.cursor()

        if user_exists(username):
            return (False, "Username {} already exists.".format(username))
        else:
            pw_hash = generate_password_hash(password)
            command = "INSERT INTO profiles (username, password) VALUES(?, ?);"
            c.execute(command, (username, pw_hash))

        db.commit()
    return (True, "Successfully registered {}".format(username))

def user_exists(username):
    '''
    Returns whether a user with the given username exists
    '''
    with sqlite3.connect("cyber.db") as db:
        c = db.cursor()

        command = "SELECT * FROM profiles WHERE username = ?"
        c.execute(command, (username,))

        return len(c.fetchall()) > 0

def login_user(username, password):
    '''
    Attempts to log in a user by checking the users table.
    Returns a tuple containing a boolean indicating success
    and a message to flash to the user.
    '''
    if username == '' or password == '':
        return (False, "Username or password missing!")

    with sqlite3.connect("cyber.db") as db:
        c = db.cursor()
        command = "SELECT username, password FROM profiles;"
        c.execute(command)
        for user in c:
            if user and username == user[0]:
                if check_password_hash(user[1], password):
                    return (True, "Successfully logged in!")
    return (False, "Incorrect username or password.")

def is_loggedin(session):
    '''
    Given a session, returns the username of the user if the user is logged in.
    Otherwise, returns False.
    '''
    if session.get('loggedin') is None:
        return False
    return session.get('loggedin')

def get_userid(session):
    name = is_loggedin(session)
    with sqlite3.connect("cyber.db") as db:
        c = db.cursor()
        command = "SELECT userid FROM profiles WHERE username = ?"
        c.execute(command, (name,))
        return c.fetchone()[0]
