from flask import Flask, render_template, request, flash, redirect, url_for
import re
from flask_mail import Mail, Message

import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')

# Flask-Mail configuration (replace with your actual email server details)
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'your_email@example.com'
app.config['MAIL_PASSWORD'] = 'your_email_password'
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@example.com'
mail = Mail(app)

# Home route for both regex matching and email validation
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        test_string = request.form.get("test_string")
        regex_pattern = request.form.get("regex_pattern")

        matched_strings = re.findall(regex_pattern, test_string)

        return render_template("index.html", test_string=test_string, regex_pattern=regex_pattern, matches=matched_strings)

    return render_template("index.html")

# Email validation route
@app.route("/validate_email", methods=["POST"])
def validate_email():
    email = request.form.get("email")

    # Perform email validation using a more comprehensive regex pattern
    is_valid_email = re.match(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$', email) is not None

    if is_valid_email:
        # Send a confirmation email
        send_confirmation_email(email)

    return render_template("index.html", email=email, is_valid=is_valid_email)

# Function to send a confirmation email
def send_confirmation_email(email):
    try:
        msg = Message('Email Confirmation', recipients=[email])
        msg.body = 'Thank you for signing up! Your email has been verified.'
        mail.send(msg)

        flash('A confirmation email has been sent to your address.', 'success')

    except Exception as e:
        flash('Error sending confirmation email. Please try again later.', 'danger')
        print(str(e))

    # Redirect to the home page
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
