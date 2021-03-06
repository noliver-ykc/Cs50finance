import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd


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

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # user_id = session['user_id']
    # portfolio = db.execute("SELECT * FROM portfolio WHERE user_id = :user_id GROUP BY stock", user_id = user_id)
    # data = {
    #     'balance': db.execute("SELECT cash FROM users where id = :user_id", user_id = user_id)[0]['cash'],
    #     'owned': stocksCurPrice(stocks),
    # }
    # data['stockBalance'] = TotalBalance(data['owned'])
    # stocks = db.execute("SELECT * FROM transactions where user_id = :user_id ORDER BY date DESC", user_id = user_id)
    # data['stocks'] = stocksCurPrice(stocks)
    # return data

    #return apology("TODO")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    return apology("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct #password was changed to pswd_hash by me
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        #let them know they logged in
        flash('You were successfully logged in')

        # Redirect user to home page
        return render_template("index.html")

        # OR
        # return redirect(url_for("index"))

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # let them know theyve been logged out
    flash("Log out successful")
    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    return apology("TODO")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        """Register user"""
        return render_template("register.html")

    if request.method == "POST":
        if not request.form.get("pswd") == request.form.get("pswd_match"):
            return apology("passwords do not match", 400)


        #hash password
        pswd_hash = generate_password_hash(request.form.get("pswd"))

        # insert data into db
        result = db.execute("INSERT INTO users (username, email, hash) VALUES(:username, :email, :pswd_hash)", username=request.form.get("username"), email=request.form.get("email"), pswd_hash=pswd_hash)
        # check that email / username does not already exist
        if not result:
            return apology("An account with that username/email already exists")

        # Remember that user is logged in
        session["user_id"] = result

        # account successful, redirect index
        flash('You have successfully registered for CS50 finance')
        # return redirect(url_for('index'))

        return render_template("index.html")




@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)