import os
import re
import openai
from flask import Flask, render_template, redirect, url_for, flash, session, request, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")
openai.api_key = os.environ.get("OPENAI_API_KEY")


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


@app.context_processor
def inject_user():
    if "user" in session:
        user = mongo.db.users.find_one({"email": session["user"]})
        return dict(logged_in_user=user)
    return dict(logged_in_user=None)


@app.route("/update_email_page/<email>")
def update_email_page(email):
    if "user" in session and session["user"] == email:
        user = mongo.db.users.find_one({"email": email})
        if user:
            return render_template("profile-update.html", user=user)
        else:
            flash("User not found.")
            return redirect(url_for("login"))
    else:
        flash("You need to log in to update your email.")
        return redirect(url_for("login"))


@app.route("/update_email/<email>", methods=["POST"])
def update_email(email):
    if "user" in session and session["user"] == email:
        new_email = request.form.get("new_email").lower()
        existing_user = mongo.db.users.find_one({"email": new_email})
        if existing_user:
            flash("Email already in use. Please choose a different one.")
            return redirect(url_for("update_email_page", email=email))
        
        mongo.db.users.update_one(
            {"email": email},
            {"$set": {"email": new_email}}
        )

        session["user"] = new_email
        flash("Email updated successfully!")
        return redirect(url_for("profile", email=new_email))
    else:
        flash("You need to log in to update your email.")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # Remove user from session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


# Handle the reading request
@app.route("/tarot_reading", methods=["POST"])
def tarot_reading():
    if request.method == "POST":
        user_choice = request.form.get("tarot_choice")
        user_question = request.form.get("question")
        user = mongo.db.users.find_one({"email": session["user"]})

        # Fetch cards from database
        cards = list(mongo.db.tarotCards.find())
        
        # Select cards based on user's choice
        if user_choice == "General":
            selected_cards = random.sample(cards, 3)
        elif user_choice == "Love":
            selected_cards = random.sample(cards, 5)
        elif user_choice == "Career":
            selected_cards = random.sample(cards, 6)
        else:
            flash("Invalid choice")
            return redirect(url_for("get_cards"))

        # Prepare the prompt for ChatGPT
        system_message = {
            "role": "system",
            "content": "You are a Tarot Reader. Your name is Sebastian Oracle. Speak to the user as a reader and use their first name. Do their tarot reading."
        }
        user_message = {
            "role": "user",
            "content": f"""
            User's name: {user['first_name']} {user['last_name']}
            Date of birth: {user['date_of_birth']}
            Time of birth: {user['time_of_birth']}
            Place of birth: {user['place_of_birth']}
            Question: {user_question}
            Tarot spread: {"Three-Card Spread" if user_choice == "General" else "Five-Card Spread" if user_choice == "Love" else "Six-Card Spread"}
            {"Card position past: " + selected_cards[0]["cardName"]}
            {"Card position present: " + selected_cards[1]["cardName"]}
            {"Card position future: " + selected_cards[2]["cardName"]}
            {"Card position advice: " + selected_cards[3]["cardName"] if user_choice in ["Love", "Career"] else ""}
            {"Card position potential outcomes: " + selected_cards[4]["cardName"] if user_choice in ["Love", "Career"] else ""}
            {"Card position cause: " + selected_cards[5]["cardName"] if user_choice == "Career" else ""}
            """
        }

        # ChatGPT API call
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[system_message, user_message]
        )

        reading_output = response.choices[0].message['content']

        return jsonify({
            "selected_cards": selected_cards,
            "reading_output": reading_output
        })


@app.route("/reading")
def reading():
    return render_template("reading.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
