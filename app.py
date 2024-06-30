import os
from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)



# class RegisterForm(FlaskForm):
#     email = StringField('Email', validators=[InputRequired(), Email()])
#     first_name = StringField('First Name', validators=[InputRequired()])
#     last_name = StringField('Last Name', validators=[InputRequired()])
#     dob = DateField('Date of Birth', validators=[InputRequired()])
#     place_of_birth = StringField('Place of Birth', validators=[InputRequired()])
#     time_of_birth = TimeField('Time of Birth (if known)')
#     password = PasswordField('Password', validators=[InputRequired(), EqualTo('confirm', message='Passwords must match')])
#     confirm = PasswordField('Confirm Password')
#     submit = SubmitField('Register')


# class LoginForm(FlaskForm):
#     email = StringField('Email', validators=[InputRequired(), Email()])
#     password = PasswordField('Password', validators=[InputRequired()])
#     submit = SubmitField('Login')


@app.route("/")
@app.route("/get_cards")
def get_cards():
    cards = list(mongo.db.tarotCards.find())
    return render_template("index.html", cards=cards)


@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
