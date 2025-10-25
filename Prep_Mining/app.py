from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
import bcrypt
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'flaskuser'
app.config['MYSQL_PASSWORD'] = 'Sai@123456'
app.config['MYSQL_DB'] = 'flaskapplication'
app.secret_key = 'your_secret_key_here'

mysql = MySQL(app)

class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register") 

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register") 

@app.route('/')
def idel():
    return "Welcome to Prep_Mining"
    
@app.route('/Home')
def dashboard():
    return render_template('dashboard.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()  # ✅ instantiate form

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        # ✅ Hash password properly
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # ✅ Store data into database
        cursor = mysql.connection.cursor()
        
         # Check if user with same email already exists
        cursor.execute("SELECT * FROM user WHERE email=%s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Email already registered. Please login.', 'danger')
            cursor.close()
            return redirect(url_for('login'))

        # Insert new user
        cursor.execute(
            "INSERT INTO user (name, email, password) VALUES (%s, %s, %s)",
            (name, email, hashed_password)
        )
        mysql.connection.commit()
        cursor.close()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/login',  methods=['GET', 'POST'])
def login():
    form = LoginForm()  # ✅ instantiate form

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT * FROM user WHERE email= %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            session['user_id'] = user[0]
            return redirect(url_for('elements'))
        else:
            flash(" login Failed ")
            return redirect(url_for('login'))
    
    return render_template('login.html', form=form)

@app.route('/elements')
def elements():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))
    return render_template('elements.html')

@app.route('/generic')
def generic():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))
    return render_template('generic.html')

@app.route('/index')
def index():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
