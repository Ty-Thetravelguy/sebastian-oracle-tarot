import os
from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, TimeField
from wtforms.validators import InputRequired, Email, EqualTo
from flask_bcrypt import Bcrypt

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)
bcrypt = Bcrypt(app)


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    dob = DateField('Date of Birth', validators=[InputRequired()])
    place_of_birth = StringField('Place of Birth', validators=[InputRequired()])
    time_of_birth = TimeField('Time of Birth (if known)')
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password')
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')


@app.route("/")
@app.route("/get_cards")
def get_cards():
    cards = list(mongo.db.tarotCards.find())
    return render_template("index.html", cards=cards)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login handler"""
    if session.get('logged_in'):
        if session['logged_in'] is True:
            return redirect(url_for('index', title="Sign In"))

    form = LoginForm()

    if form.validate_on_submit():
        # get all users
        users = mongo.db.users
        # try and get one with same email as entered
        db_user = users.find_one({'email': request.form['email']})

        if db_user:
            # check password using hashing
            if bcrypt.check_password_hash(db_user['password'], request.form['password']):
                session['email'] = request.form['email']
                session['logged_in'] = True
                # successful redirect to home logged in
                return redirect(url_for('get_cards'))
            # must have failed set flash message
            flash('Invalid email/password combination')
    return render_template("login.html", title="Sign In", form=form)


@app.route('/logout')
def logout():
    """Clears session and redirects to home"""
    session.clear()
    return redirect(url_for('get_cards'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handles registration functionality"""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        # get all the users
        users = mongo.db.users
        # see if we already have the entered email
        existing_user = users.find_one({'email': request.form['email']})

        if existing_user is None:
            # hash the entered password
            hash_pass = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
            # insert the user to DB
            users.insert_one({
                'email': request.form['email'],
                'password': hash_pass,
                'first_name': request.form['first_name'],
                'last_name': request.form['last_name'],
                'dob': request.form['dob'],
                'place_of_birth': request.form['place_of_birth'],
                'time_of_birth': request.form['time_of_birth']
            })
            session['email'] = request.form['email']
            session['logged_in'] = True
            return redirect(url_for('get_cards'))
        # duplicate email set flash message and reload page
        flash('Sorry, that email is already registered - use another')
        return redirect(url_for('register'))
    return render_template('register.html', title='Register', form=form)


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/saved_readings')
def saved_readings():
    return render_template('saved_readings.html')


@app.route('/journal')
def journal():
    return render_template('journal.html')


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
