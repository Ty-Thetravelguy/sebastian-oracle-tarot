import os
import re
import random
import openai
from flask import Flask, render_template, redirect, url_for, flash, session, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

# Flask app configuration
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Password validation function
def validate_password(password):
    pattern = r"^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};:\\\|,.<>\/?]).{6,20}$"
    return re.match(pattern, password) is not None

# Home route to get cards
@app.route("/")
@app.route("/get_cards")
def get_cards():
    cards = list(mongo.db.tarotCards.find())
    return render_template("index.html", cards=cards)

# User registration route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one({"email": request.form.get("email").lower()})

        if existing_user:
            flash("USER ALREADY EXISTS")
            return redirect(url_for("register"))
        
        password = request.form.get("password")
        password_repeat = request.form.get("password_repeat")
        if password != password_repeat:
            flash("Passwords do not match")
            return redirect(url_for("register"))
        
        if not validate_password(password):
            flash("Password must be between 6 and 20 characters long, contain at least one uppercase letter, one number, and one special character.")
            return redirect(url_for("register"))

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

        session["user"] = request.form.get("email").lower()
        flash("Registration Successful!")
        return redirect(url_for("get_cards"))

    return render_template("register.html")

# User login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one({"email": request.form.get("email").lower()})

        if existing_user:
            if check_password_hash(existing_user["password"], request.form.get("password")):
                session["user"] = existing_user["email"]
                flash("Welcome, {}".format(existing_user["first_name"]))
                return redirect(url_for("get_cards"))

            flash("Incorrect email and/or password!")
            return redirect(url_for("login"))

        flash("Incorrect email and/or password!")
        return redirect(url_for("login"))

    return render_template("login.html")

# User profile route
@app.route("/profile/<email>")
def profile(email):
    if "user" in session and session["user"] == email:
        user = mongo.db.users.find_one({"email": email})
        if user:
            return render_template("profile.html", user=user)
        flash("User not found.")
        return redirect(url_for("login"))
    
    flash("You need to log in to view your profile.")
    return redirect(url_for("login"))

# Inject logged in user into templates
@app.context_processor
def inject_user():
    if "user" in session:
        user = mongo.db.users.find_one({"email": session["user"]})
        return dict(logged_in_user=user)
    return dict(logged_in_user=None)

# Route to update email page
@app.route("/update_email_page/<email>")
def update_email_page(email):
    if "user" in session and session["user"] == email:
        user = mongo.db.users.find_one({"email": email})
        if user:
            return render_template("profile-update.html", user=user)
        flash("User not found.")
        return redirect(url_for("login"))
    else:
        flash("You need to log in to update your email.")
        return redirect(url_for("login"))

# Update email logic
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

# User logout route
@app.route("/logout")
def logout():
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))

# Loading page route
@app.route("/loading")
def loading():
    return render_template("loading.html")

# Process tarot reading request
@app.route("/process_tarot_reading", methods=["POST"])
def process_tarot_reading():
    try:
        data = request.json
        user_choice = data.get("tarot_choice")
        user_question = data.get("question")
        user = mongo.db.users.find_one({"email": session["user"]})

        cards = list(mongo.db.tarotCards.find())

        if user_choice == "General":
            selected_cards = random.sample(cards, 3)
        elif user_choice == "Love":
            selected_cards = random.sample(cards, 5)
        elif user_choice == "Career":
            selected_cards = random.sample(cards, 6)
        else:
            return jsonify({"success": False, "message": "Invalid choice"})

        selected_cards = [convert_objectid_to_string(card) for card in selected_cards]

        messages = [
            {
                "role": "system",
                "content": "You are a Tarot Reader. Your name is Sebastian Oracle. Speak to the user as a reader and use their first name. Do their tarot reading."
            },
            {
                "role": "user",
                "content": f"""
                User's name: {user['first_name']}
                Date of birth: {user['date_of_birth']}
                Time of birth: {user['time_of_birth']}
                Place of birth: {user['place_of_birth']}
                Question: {user_question}
                Tarot spread: {"Three-Card Spread" if user_choice == "General" else "Five-Card Spread" if user_choice == "Love" else "Six-Card Spread"}
                Card position past: {selected_cards[0]["cardName"]}
                Card position present: {selected_cards[1]["cardName"]}
                Card position future: {selected_cards[2]["cardName"]}
                {"Card position advice: " + selected_cards[3]["cardName"] if user_choice in ["Love", "Career"] else ""}
                {"Card position potential outcomes: " + selected_cards[4]["cardName"] if user_choice in ["Love", "Career"] else ""}
                {"Card position cause: " + selected_cards[5]["cardName"] if user_choice == "Career" else ""}
                """
            }
        ]

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages
        )

        reading_output = response['choices'][0]['message']['content']

        return jsonify({"success": True, "selected_cards": selected_cards, "reading_output": reading_output})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# Route to display tarot reading
@app.route("/reading")
def reading():
    cards = session.get("selected_cards", [])
    reading_output = session.get("reading_output", "")

    if not cards or not reading_output:
        flash("No reading found. Please submit your question again.")
        return redirect(url_for("get_cards"))

    return render_template("reading.html", cards=cards, reading_output=reading_output)

# Convert ObjectId to string
def convert_objectid_to_string(doc):
    doc['_id'] = str(doc['_id'])
    return doc

# Run the app
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
