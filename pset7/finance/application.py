import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Ensure environment variable is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Style guide on breaking up long lines
# https://www.python.org/dev/peps/pep-0008/#maximum-line-length


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Access portfolio of stocks
    user_stocks = db.execute("SELECT * FROM portfolio WHERE id = :id", id=session["user_id"])

    net_worth = 0
    for row in user_stocks:
        # Get stock symbol
        symbol = row["symbol"]
        # Update total price of owned shares
        total = row["price"] * row["shares"]
        # Update portfolio with new total
        db.execute("UPDATE portfolio SET total = :total WHERE id = :id AND symbol = :symbol",
                   total=total, id=session["user_id"], symbol=symbol)
        # Add stocks updated total to net_worth
        net_worth += row["total"]

    # Get user cash
    user_cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])

    # Calculate grand total
    net_worth += user_cash[0]["cash"]

    # Display table of owned stocks and net worth
    return render_template("index.html", stocks=user_stocks, cash=user_cash[0]["cash"], net_worth=net_worth)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get stock info by lookup
        stock = lookup(request.form.get("symbol"))
        if not stock:
            return apology("Stock not found")

        # Get share number by lookup
        # Try-except to check for correct share input https://docs.python.org/3/tutorial/errors.html
        try:
            shares = int(request.form.get("shares"))
            if shares < 0:
                return apology("Enter positive number of shares")
        except:
            return apology("Enter number of shares")

        # Get users cash
        cash = db.execute("SELECT cash FROM users WHERE id = :id",
                          id=session["user_id"])

        # Total cost of stock purchase
        cost = stock["price"] * shares
        if cash[0]["cash"] - cost < 0:
            return apology("Shares greater than cash available")

        # Add purchase to user history
        db.execute("INSERT INTO history(id, symbol, shares, price) \
                    VALUES(:id, :symbol, :shares, :price)", id=session["user_id"],
                   symbol=stock["symbol"], shares=shares, price=stock["price"])

        # Update cash in users table
        db.execute("UPDATE users SET cash = cash - :cost WHERE id = :id",
                   cost=cost, id=session["user_id"])

        # Checking if stock is in user portfolio
        user_stock = db.execute("SELECT shares FROM portfolio WHERE id = :id \
                                AND symbol = :symbol", id=session["user_id"],
                                symbol=stock["symbol"])

        # If shares not in portfolio, create new row in portfolio
        if not user_stock:
            db.execute("INSERT INTO portfolio(id, symbol, shares, price, total) \
                        VALUES(:id, :symbol, :shares, :price, :total)",
                       id=session["user_id"], symbol=stock["symbol"],
                       shares=shares, price=stock["price"], total=cost)

        # Otherwise add purchased shares to existing shares in portfolio
        else:
            db.execute("UPDATE portfolio SET shares=:shares WHERE id=:id \
                        AND symbol=:symbol", shares=user_stock[0]["shares"] + shares,
                       id=session["user_id"], symbol=stock["symbol"])

        # Return user to homepage
        return redirect("/")

    # User reached via GET (clicking link or redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Get transactions for current user
    history = db.execute("SELECT * FROM history WHERE id = :id", id=session["user_id"])
    return render_template("history.html", stocks=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get stock info by lookup
        result = lookup(request.form.get("symbol"))
        if not result:
            return apology("Stock not found")

        # Redirect user to page displaying stock quote
        return render_template("quoted.html", symbol=result["symbol"], price=usd(result["price"]))

    # User reached via GET (clicking link or redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Check password matches confirm password
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must match")

        # Hash password
        hashed = generate_password_hash(request.form.get("password"),
                                        method='pbkdf2:sha256', salt_length=8)

        # Add username and password to database
        result = db.execute("INSERT INTO users(username, hash) VALUES(:username, :hash)",
                            username=request.form.get("username"), hash=hashed)
        if not result:
            return apology("username must be unique")

        # Once registered, log in automatically
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Return user to homepage
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


# Personal touch, allow user's to change their password once registered
@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    """Change the user's password"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get user's saved password hash from table
        user_pass = db.execute("SELECT hash FROM users WHERE id = :id",
                               id=session["user_id"])

        # Check stored password to entered password
        if not check_password_hash(user_pass[0]["hash"], request.form.get("password-old")):
            return apology("Password entered doesn't match saved password")

        # Check new password exists and matches confirmation
        if not request.form.get("password-new"):
            return apology("Enter new password")

        elif request.form.get("password-new") != request.form.get("confirmation"):
            return apology("New password doesn't match confirmation")

        # Hash new password
        hashed = generate_password_hash(request.form.get("password-new"),
                                        method='pbkdf2:sha256', salt_length=8)

        # Update users table set password = hashed new password
        db.execute("UPDATE users SET hash = :hash WHERE id = :id", hash=hashed, id=session["user_id"])

        # Flash message and log user out
        flash("Password successfully changed!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("change.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # If user reached method via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get symbol selected
        symbol = request.form.get("symbol")

        # Check symbol is in portfolio
        user_stock = db.execute("SELECT * FROM portfolio WHERE id = :id AND symbol = :symbol",
                                id=session["user_id"], symbol=symbol)
        if not user_stock:
            return apology("Stock not found in portfolio")

        # Get number of shares entered
        sell_shares = int(request.form.get("shares"))
        user_shares = user_stock[0]["shares"]

        # Lookup current price of selected symbol
        new_price = lookup(symbol)
        # Sale price * shares = money to add to portfolio
        sale = new_price["price"] * float(sell_shares)

        # Check shares entered isn't greater than actual shares
        if sell_shares > user_shares:
            return apology("Selling more shares than owned")

        # If selling less than total amount of shares
        elif sell_shares < user_shares:
            # Add row to history with sale of stock (negative shares)
            db.execute("INSERT INTO history(id, symbol, shares, price) \
                    VALUES(:id, :symbol, :shares, :price)", id=session["user_id"],
                       symbol=symbol, shares=sell_shares * -1, price=new_price["price"])
            # Update portfolio with sale
            db.execute("UPDATE portfolio SET shares = shares - :shares WHERE id = :id \
                        AND symbol = :symbol", shares=sell_shares, id=session["user_id"],
                       symbol=symbol)

        else:
            # Selling all possible shares
            # Add row to history table with sale of stock (negative shares)
            db.execute("INSERT INTO history(id, symbol, shares, price) \
                    VALUES(:id, :symbol, :shares, :price)", id=session["user_id"],
                       symbol=symbol, shares=sell_shares * -1, price=new_price["price"])
            # Delete stock from portfolio table
            db.execute("DELETE FROM portfolio WHERE id = :id AND symbol = :symbol",
                       id=session["user_id"], symbol=symbol)

        # Update cash in users table
        db.execute("UPDATE users SET cash = cash + :sale WHERE id = :id",
                   sale=sale, id=session["user_id"])

        # Return user to homepage
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        user_stocks = db.execute("SELECT * FROM portfolio WHERE id =:id", id=session["user_id"])
        return render_template("sell.html", stocks=user_stocks)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
