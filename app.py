import os
import re
from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash


if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


# Password Validation Function
def validate_password(password):
    pattern = r"^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};:\\\|,.<>\/?]).{6,20}$"
    if re.match(pattern, password):
        return True
    else:
        return False

@app.route("/")
@app.route("/get_cards")
def get_cards():
    cards = list(mongo.db.tarotCards.find())
    return render_template("index.html", cards=cards)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Check if username already exists in DB
        existing_user = mongo.db.users.find_one(
            {"email": request.form.get("email").lower()})

        # If user exists - show message
        if existing_user:
            flash("USER ALREADY EXISTS")
            return redirect(url_for("register"))
        
        # Check if passwords match
        password = request.form.get("password")
        password_repeat = request.form.get("password_repeat")
        if password != password_repeat:
            flash("Passwords do not match")
            return redirect(url_for("register"))
        
        # Validate password strength
        if not validate_password(password):
            flash("Password must be between 6 and 20 characters long, contain at least one uppercase letter, one number, and one special character.")
            return redirect(url_for("register"))

        # If passwords match and valid, proceed with registration
        register = {
            "first_name": request.form.get("first_name").capitalize(),
            "last_name": request.form.get("last_name").capitalize(),
            "email": request.form.get("email").lower(),
            "date_of_birth": request.form.get("date_of_birth"),
            "time_of_birth": request.form.get("time_of_birth"),
            "place_of_birth": request.form.get("place_of_birth").capitalize(),
            "password": generate_password_hash(password)
        }
        mongo.db.users.insert_one(register)

        # Put the new user into 'session' cookie
        session["user"] = request.form.get("email").lower()
        flash("Registration Successful!")
        return redirect(url_for("get_cards"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Check if user exists in db
        existing_user = mongo.db.users.find_one(
            {"email": request.form.get("email").lower()})

        if existing_user:
            # Ensure hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = existing_user["email"]
                    flash("Welcome, {}".format(existing_user["first_name"]))
                    return redirect(url_for("get_cards"))

            else:
                # Invalid password
                flash("Incorrect email and/or password!")
                return redirect(url_for("login"))

        else:
            # User doesn't exist
            flash("Incorrect email and/or password!")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<email>")
def profile(email):
    # Checks if the user is logged in and if the logged-in 
    # user's email matches the email in the URL
    if "user" in session and session["user"] == email:
        user = mongo.db.users.find_one({"email": email})
        if user:
            # If the user is found in the database
            return render_template("profile.html", user=user)
        else:
            # If no user is found, flash a message and redirect to the login page
            flash("User not found.")
            return redirect(url_for("login"))
    else:
        # If the user is not logged in or trying to access a different user's profile
        flash("You need to log in to view your profile.")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # Remove user from session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)