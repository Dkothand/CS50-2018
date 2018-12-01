import sqlite3

from flask import Flask, flash, g, jsonify, redirect, render_template, request, session
from helpers import login_required
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

app.secret_key = '_5#y2L"F4Q8z\n\xec]/'


# http://flask.pocoo.org/docs/dev/tutorial/setup/
def connect_db():
    """Connect to database"""
    db = sqlite3.connect('schedule.db')

    # Configure to return dictionary instead of tuple
    db.row_factory = sqlite3.Row
    return db


# http://flask.pocoo.org/docs/dev/tutorial/dbcon/
def get_db():
    """Opens new database connection for current
    application context if none exists yet.
    """
    if not hasattr(g, 'schedule.db'):
        g.schedule_db = connect_db()
    return g.schedule_db


# http://flask.pocoo.org/docs/dev/tutorial/dbcon/
@app.teardown_appcontext
def close_db(error):
    """Closes database at the end of a request"""
    if hasattr(g, 'schedule.db'):
        g.schedule_db.close()


@app.before_request
def logged_in():
    """Checks if user is logged in, works with login_required decorator"""
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()


@app.route('/')
def welcome():
    """Welcome page"""
    return render_template("welcome.html")


@app.route("/logout")
def logout():
    """Logs user out"""
    session.clear()
    flash("You are logged out")
    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def log_in():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # If user submits information via POST request
    if request.method == 'POST':

        # Message for error flashing
        error = None

        # Connect to database
        db = get_db()

        # Query database for login credentials
        user = db.execute("SELECT * FROM users WHERE username = ?", (request.form['username'],)).fetchone()

        if user is None or not check_password_hash(user["psw"], request.form['password']):
            error = "Invalid credentials"

        if error is None:
            # Remember that user is logged in
            session['user_id'] = user['id']
            return redirect("/homepage")

    # GET request
    else:
        error = "Please log in by clicking Log In"

    flash(error)
    return render_template("welcome.html")


@app.route("/homepage", methods=["GET", "POST"])
@login_required
def home_page():
    """Homepage when user logs in"""
    return render_template("homepage.html")


# http://flask.pocoo.org/docs/1.0/tutorial/views/
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # If user submits information via POST request
    if request.method == "POST":

        # Message for error flashing
        error = None

        # Open connection to db
        db = get_db()

        # Get credentials
        user = request.form['username']
        psw = request.form['password']

        # Username, password, and confirmation can't be blank
        if not user:
            error = "Please enter a username"
        elif not psw:
            error = "Please enter a password"
        elif not request.form['confirmation']:
            error = "Please enter confirmation password"

        # Password and Confirmation must match
        elif psw != request.form['confirmation']:
            error = "Confirmation must match password"

        # User can't already be registered
        elif db.execute("SELECT id FROM users WHERE username = ?", (user,)).fetchone() is not None:
            error = "Username is already registered"

        # Hash password
        hashed = generate_password_hash(psw)

        # Insert entries into users table
        if error is None:
            db.execute("INSERT INTO users(username, psw) VALUES(?, ?)", (user, hashed))
            db.commit()
            error = "You are registered! Please log in"

        # Redirect to welcome with success message
        flash(error)
        return redirect('/')

    # Else return to welcome page
    else:
        error = "Please register an account by clicking Register"
        flash(error)
        return render_template("welcome.html")


@app.route("/_create", methods=["POST"])
@login_required
def create_event():
    """Inserts FullCalendar event into database via ajax request"""

    # Open db connection
    db = get_db()

    # Get event data
    title = request.form['title']
    start = request.form['start']
    end = request.form['end']

    # Insert event data into events table
    db_row = db.execute("INSERT INTO events(title, start, end, user_id) VALUES(?, ?, ?, ?)",
                        (title, start, end, session["user_id"]))
    db.commit()

    # Get id of inserted row to send to client side
    row_id = db_row.lastrowid

    # Return JSON to client-side
    return jsonify({'id': row_id, 'title': title, 'start': start, 'end': end})


@app.route("/_remove", methods=["POST"])
@login_required
def remove_event():
    """Removes FullCalendar event from database via ajax request"""

    # Open db connection
    db = get_db()

    row_id = request.form['id']

    # Remove event from database with cooresponding event id
    db.execute("DELETE FROM events WHERE id = ?", (row_id,))
    db.commit()

    # Return event id to client side for removal
    return jsonify({'id': row_id})


@app.route("/_update", methods=["POST"])
@login_required
def update_event():
    """Updates FullCalendar event from database via ajax request"""

    # Open db connection
    db = get_db()

    # Get event id
    title = request.form['title']
    row_id = request.form['id']

    # Remove event from database with cooresponding event id
    db.execute("UPDATE events SET title = ? WHERE id = ?", (title, row_id))
    db.commit()

    # Return title for client alert
    return jsonify({'title': title})


@app.route("/_drop", methods=["POST"])
@login_required
def event_drop():
    """Updates database when event is dropped to new time frame via ajax request"""

    # Open db connection
    db = get_db()

    # Get event title, id, start and end times
    start = request.form['start']
    end = request.form['end']
    row_id = request.form['id']

    # Remove event from database with cooresponding event id
    db.execute("UPDATE events SET start = ?, end = ? WHERE id = ?", (start, end, row_id))
    db.commit()

    # Return event title for client alert
    return jsonify({'title': request.form['title']})


@app.route("/_events", methods=["GET"])
@login_required
def get_events():
    """Generates JSON to send to client for event-rendering on login"""

    # Open db connection
    db = get_db()

    # Get event title, id, start and end time where user_id is equal to session_id (user that's logged in)
    # rows is cursor object
    rows = db.execute("SELECT id, title, start, end FROM events WHERE user_id = ?", (session['user_id'],))
    event_rows = rows.fetchall()

    # Build array of rows from db by iterating over returned rows
    events = [{'id': row[0], 'title': row[1], 'start': row[2], 'end': row[3]} for row in event_rows]

    # return array of json's with jsonify
    return jsonify(events)