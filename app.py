import os
import re
import random
import openai
import datetime
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


# Date parsing function
def safe_parse_date(date_string):
    try:
        return datetime.datetime.strptime(date_string, "%Y-%m-%d").strftime("%B %d, %Y")
    except Exception as e:
        return date_string


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


# Form submission for tarot reading
@app.route("/submit_tarot_form", methods=["POST"])
def submit_tarot_form():
    try:
        tarot_choice = request.form.get("tarot_choice")
        question = request.form.get("question")
        
        session["tarot_choice"] = tarot_choice
        session["question"] = question
        
        return redirect(url_for("loading"))
    except Exception as e:
        flash("An error occurred while processing your request. Please try again.")
        return redirect(url_for("get_cards"))


# Process tarot reading request
@app.route("/process_tarot_reading", methods=["POST"])
def process_tarot_reading():
    try:
        if "user" not in session:
            return jsonify({"success": False, "message": "User not logged in"})
        
        tarot_choice = session.get("tarot_choice")
        question = session.get("question")
        user = mongo.db.users.find_one({"email": session["user"]})

        if not user:
            return jsonify({"success": False, "message": "User not found"})

        cards = list(mongo.db.tarotCards.find())

        if tarot_choice == "General":
            selected_cards = random.sample(cards, 3)
        elif tarot_choice == "Love":
            selected_cards = random.sample(cards, 5)
        elif tarot_choice == "Career":
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
                Question: {question}
                Tarot spread: {"Three-Card Spread" if tarot_choice == "General" else "Five-Card Spread" if tarot_choice == "Love" else "Six-Card Spread"}
                Card position past: {selected_cards[0]["cardName"]}
                Card position present: {selected_cards[1]["cardName"]}
                Card position future: {selected_cards[2]["cardName"]}
                {"Card position advice: " + selected_cards[3]["cardName"] if tarot_choice in ["Love", "Career"] else ""}
                {"Card position potential outcomes: " + selected_cards[4]["cardName"] if tarot_choice in ["Love", "Career"] else ""}
                {"Card position cause: " + selected_cards[5]["cardName"] if tarot_choice == "Career" else ""}
                """
            }
        ]

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages
        )

        reading_output = response['choices'][0]['message']['content']

        # Save reading data to session
        session["selected_cards"] = selected_cards
        session["reading_output"] = reading_output

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


# Save reading route
@app.route("/save_reading", methods=["POST"])
def save_reading():
    try:
        data = request.json
        reading_date = data.get("readingDate")
        question_asked = data.get("questionAsked")
        reading_data = data.get("readingData")
        category = data.get("category")

        user = mongo.db.users.find_one({"email": session["user"]})

        saved_reading = {
            "user_id": user["_id"],
            "readingDate": reading_date,
            "questionAsked": question_asked,
            "readingData": reading_data,
            "category": category
        }
        mongo.db.savedReadings.insert_one(saved_reading)

        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# Delete reading route
@app.route("/delete_reading", methods=["POST"])
def delete_reading():
    try:
        data = request.json
        reading_id = data.get("readingId")

        mongo.db.savedReadings.delete_one({"_id": ObjectId(reading_id)})

        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# Route to get saved readings
@app.route("/saved_readings/<email>")
def saved_readings(email):
    if "user" in session and session["user"] == email:
        user = mongo.db.users.find_one({"email": email})
        if user:
            saved_readings = list(mongo.db.savedReadings.find({"user_id": user["_id"]}).sort("readingDate", -1))
            for reading in saved_readings:
                reading["_id"] = str(reading["_id"])
                reading["formatted_readingDate"] = safe_parse_date(reading.get("readingDate"))
            return render_template("saved_readings.html", saved_readings=saved_readings)
        flash("User not found.")
        return redirect(url_for("login"))
    flash("You need to log in to view your saved readings.")
    return redirect(url_for("login"))



# Route to save journal entry
@app.route("/save_journal", methods=["POST"])
def save_journal():
    try:
        data = request.json
        reading_id = data.get("readingId")
        journal_subject = data.get("journalSubject")
        journal_date = data.get("journalDate")
        journal_text = data.get("journalText")

        mongo.db.savedReadings.update_one(
            {"_id": ObjectId(reading_id)},
            {"$set": {
                "journal_subject": journal_subject,
                "journal_date": journal_date,
                "journal_text": journal_text
            }}
        )

        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# Route to delete journal entry
@app.route("/delete_journal", methods=["POST"])
def delete_journal():
    try:
        data = request.json
        reading_id = data.get("readingId")

        mongo.db.savedReadings.update_one(
            {"_id": ObjectId(reading_id)},
            {"$unset": {
                "journal_subject": "",
                "journal_date": "",
                "journal_text": ""
            }}
        )

        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# Convert ObjectId to string
def convert_objectid_to_string(doc):
    doc['_id'] = str(doc['_id'])
    return doc


# Run the app
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
