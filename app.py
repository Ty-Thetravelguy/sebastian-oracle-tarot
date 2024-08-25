import os
import re
import random
import openai
import datetime
from bson import ObjectId
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, redirect, url_for, flash, \
session, request, jsonify


if os.path.exists("env.py"):
    import env

app = Flask(__name__)


# Flask app configuration
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)
openai.api_key = os.environ.get("OPENAI_API_KEY")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


def validate_password(password):
    """
    Validate a password to ensure it meets security requirements.

    Args:
    password (str): The password to validate.

    Returns:
    bool: True if the password is valid, False otherwise.
    """
    pattern = (
        r"^"
        r"(?=.*[A-Z])"
        r"(?=.*\d)"
        r"(?=.*[!@#$%^&*()_+\-=\[\]{};:\\|,.<>/?])"
        r".{6,20}"
        r"$"
    )
    return re.match(pattern, password) is not None


def safe_parse_date(date_string):
    """
    Safely parse a date string into a more readable format.

    Args:
    date_string (str): The date string to parse.

    Returns:
    str: The formatted date string, or the original string if parsing fails.
    """
    try:
        return datetime.datetime.strptime(
            date_string, "%Y-%m-%d").strftime("%B %d, %Y")
    except Exception as e:
        return date_string


@app.route("/")
@app.route("/get_cards")
def get_cards():
    """
    Home route to display all tarot cards.

    Returns:
    HTML: Rendered index page with tarot cards.
    """
    cards = list(mongo.db.tarotCards.find())
    return render_template("index.html", cards=cards)


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    User registration route. Handles registration
    form submission and user creation.

    Returns:
    HTML: Rendered registration page or redirects
    to get_cards on successful registration.
    """
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"email": request.form.get("email").lower()})

        if existing_user:
            flash("USER ALREADY EXISTS")
            return redirect(url_for("register"))

        password = request.form.get("password")
        password_repeat = request.form.get("password_repeat")
        if password != password_repeat:
            flash("Passwords do not match")
            return redirect(url_for("register"))

        if not validate_password(password):
            flash(
                "Password must be between 6 and 20 characters long, "
                "contain at least one uppercase letter, one number, "
                "and one special character."
            )
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


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    User login route. Handles login form submission and user authentication.

    Returns:
    HTML: Rendered login page or redirects to get_cards on successful login.
    """
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Please provide both email and password.")
            return redirect(url_for("login"))

        existing_user = mongo.db.users.find_one({"email": email})

        if existing_user and check_password_hash(existing_user["password"], password):
            session["user"] = existing_user["email"]
            session.permanent = True
            flash("Welcome, {}".format(existing_user["first_name"]))
            return redirect(url_for("get_cards"))
        else:
            flash("Incorrect email and/or password!")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<email>")
def profile(email):
    """
    User profile route. Displays the user's profile information.

    Args:
    email (str): The email of the user.

    Returns:
    HTML: Rendered profile page or redirects to
    login if the user is not authenticated.
    """
    if "user" in session and session["user"] == email:
        user = mongo.db.users.find_one({"email": email})
        if user:
            return render_template("profile.html", user=user)
        flash("User not found.")
        return redirect(url_for("login"))

    flash("You need to log in to view your profile.")
    return redirect(url_for("login"))


@app.context_processor
def inject_user():
    """
    Injects the logged-in user's information into all templates.

    Returns:
    dict: A dictionary containing the logged-in user's information.
    """
    if "user" in session:
        user = mongo.db.users.find_one({"email": session["user"]})
        return dict(logged_in_user=user)
    return dict(logged_in_user=None)


@app.route("/profile-update/<email>")
def update_profile_page(email):
    """
    Route to display the update profile page for the user.

    Args:
    email (str): The email of the user.

    Returns:
    HTML: Rendered update-profile page or redirects
    to login if the user is not authenticated.
    """
    if "user" in session and session["user"] == email:
        user = mongo.db.users.find_one({"email": email})
        if user:
            return render_template("profile-update.html", user=user)
        flash("User not found.")
        return redirect(url_for("login"))
    flash("You need to be logged in to update your profile.")
    return redirect(url_for("login"))


@app.route("/update-profile/<email>", methods=["POST"])
def update_profile(email):
    """
    Route to handle the profile update logic for the user.

    Args:
    email (str): The current email of the user.

    Returns:
    Redirect: Redirects to the profile page on successful update,
    or back to the update page if there's an error.
    """
    if "user" in session and session["user"] == email:
        new_email = request.form.get("new_email").lower()
        new_time_of_birth = request.form.get("new_time_of_birth")

        # Check if the new email already exists (if it's different from the current one)
        if new_email != email:
            existing_user = mongo.db.users.find_one({"email": new_email})
            if existing_user:
                flash("Email already in use. Please choose a different one.")
                return redirect(url_for("profile-update", email=email))

        # Update the user's profile
        mongo.db.users.update_one(
            {"email": email},
            {"$set": {
                "email": new_email,
                "time_of_birth": new_time_of_birth
            }}
        )

        # Update session if email changed
        if new_email != email:
            session["user"] = new_email

        flash("Profile updated successfully!")
        return redirect(url_for("profile", email=new_email))
    else:
        flash("You need to be logged in to update your profile.")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    """
    User logout route. Clears the user session.

    Returns:
    HTML: Redirects to the login page.
    """
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/loading")
def loading():
    """
    Route to display the loading page.

    Returns:
    HTML: Rendered loading page.
    """
    return render_template("loading.html")


@app.route('/set_tarot_choice_and_question', methods=['POST'])
def set_tarot_choice_and_question():
    """
    Sets the user's tarot choice and question in the session.

    Returns:
    JSON: Success message.
    """
    data = request.get_json()
    session['tarot_choice'] = data['tarot_choice']
    session['question'] = data['question']
    return jsonify({"success": True})


@app.route("/process_tarot_reading", methods=["POST"])
def process_tarot_reading():
    """
    Processes the tarot reading request and
    generates a reading using OpenAI API.

    Returns:
    JSON: The selected tarot cards and reading
    output or an error message.
    """
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

        selected_cards = [
            convert_objectid_to_string(card) for card in selected_cards]

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a Tarot Reader. Your name is Sebastian Oracle. "
                    "Speak to the user as a reader and use their first name. "
                    "Do their tarot reading."
                )
            },
            {
                "role": "user",
                "content": f"""
                User's name: {user['first_name']}
                Date of birth: {user['date_of_birth']}
                Time of birth: {user['time_of_birth']}
                Place of birth: {user['place_of_birth']}
                Question: {question}
                Tarot spread: {
                    "Three-Card Spread" if tarot_choice == "General"
                    else "Five-Card Spread" if tarot_choice == "Love"
                    else "Six-Card Spread"
                }
                Card position past: {selected_cards[0]["cardName"]}
                Card position present: {selected_cards[1]["cardName"]}
                Card position future: {selected_cards[2]["cardName"]}
                {
                    "Card position advice: " + selected_cards[3]["cardName"]
                    if tarot_choice in ["Love", "Career"] else ""
                }
                {
                    f"Card position potential outcomes: "
                    f"{selected_cards[4]['cardName']}"
                    if tarot_choice in ["Love", "Career"] else ""
                }
                {
                    "Card position cause: " + selected_cards[5]["cardName"]
                    if tarot_choice == "Career" else ""
                }
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

        return jsonify(
            {
                "success": True,
                "selected_cards": selected_cards,
                "reading_output": reading_output
            }
        )
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/reading")
def reading():
    """
    Route to display the tarot reading results.

    Returns:
    HTML: Rendered reading page with the tarot cards and reading output.
    """
    cards = session.get("selected_cards", [])
    reading_output = session.get("reading_output", "")

    if not cards or not reading_output:
        flash("No reading found. Please submit your question again.")
        return redirect(url_for("get_cards"))

    return render_template(
        "reading.html", cards=cards, reading_output=reading_output
    )


@app.route("/save_reading", methods=["POST"])
def save_reading():
    """
    Saves the tarot reading data to the database.

    Returns:
    JSON: Success message and redirect URL or an error message.
    """
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

        return jsonify({"success": True, "redirect_url": url_for(
            'saved_readings', email=session["user"])})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/delete_reading", methods=["POST"])
def delete_reading():
    """
    Deletes a saved tarot reading from the database.

    Returns:
    JSON: Success message or an error message.
    """
    try:
        data = request.json
        reading_id = data.get("readingId")

        mongo.db.savedReadings.delete_one({"_id": ObjectId(reading_id)})

        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/saved_readings/<email>")
def saved_readings(email):
    """
    Route to get and display the user's saved tarot readings.

    Args:
    email (str): The email of the user.

    Returns:
    HTML: Rendered saved_readings page or redirects
    to login if the user is not authenticated.
    """
    if "user" in session and session["user"] == email:
        user = mongo.db.users.find_one({"email": email})
        if user:
            saved_readings = list(mongo.db.savedReadings.find(
                {"user_id": user["_id"]}).sort("readingDate", -1))
            for reading in saved_readings:
                reading["_id"] = str(reading["_id"])
                reading["formatted_readingDate"] = safe_parse_date(
                    reading.get("readingDate")
                )
            return render_template(
                "saved_readings.html", saved_readings=saved_readings
            )
        flash("User not found.")
        return redirect(url_for("login"))
    flash("You need to log in to view your saved readings.")
    return redirect(url_for("login"))


@app.route("/save_journal", methods=["POST"])
def save_journal():
    """
    Saves a journal entry related to a tarot reading.

    Returns:
    JSON: Success message or an error message.
    """
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


@app.route("/delete_journal", methods=["POST"])
def delete_journal():
    """
    Deletes a journal entry related to a tarot reading.

    Returns:
    JSON: Success message or an error message.
    """
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


@app.route("/delete_account", methods=["POST"])
def delete_account():
    """
    Deletes the user's account and all associated data.

    Returns:
    JSON: Success message and redirect URL or an error message.
    """
    try:
        if "user" in session:
            user_email = session["user"]
            # Delete user data
            mongo.db.users.delete_one({"email": user_email})
            # Delete user saved readings
            user = mongo.db.users.find_one({"email": user_email})
            if user:
                mongo.db.savedReadings.delete_many({"user_id": user["_id"]})
            session.pop("user")
            flash("Your account has been deleted.")
            return jsonify({"success": True, "redirect_url": url_for("login")})
        else:
            return jsonify(
                {"success": False, "message": "User not logged in."}
            ), 401
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


def convert_objectid_to_string(doc):
    """
    Convert MongoDB ObjectId to string.

    Args:
    doc (dict): The document containing the ObjectId.

    Returns:
    dict: The document with ObjectId converted to string.
    """
    doc['_id'] = str(doc['_id'])
    return doc


@app.route('/session_info')
def session_info():
    """
    Route to check session information for debugging.

    Returns:
    JSON: The current session data.
    """
    return jsonify(dict(session))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
