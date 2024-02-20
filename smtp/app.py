from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ravi4613'
app.config['MYSQL_DB'] = 'geekprofile'

mysql = MySQL(app)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Change to your SMTP server
app.config['MAIL_PORT'] = 587  # Change to the appropriate port
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ravikirang4613@gmail.com'  # Change to your email address
app.config['MAIL_PASSWORD'] = 'ssndvykkqgmoiyle'  # Change to your email password
app.config['MAIL_DEFAULT_SENDER'] = 'ravikirang4613@gmail.com'

mail = Mail(app)


@app.route('/')
def index():
    return 'Welcome to the email sender!'

@app.route('/send_email')
def send_email():
    recipient = ['20ht1a4613@gmail.com','ravikiran3532@gmail.com','20ht1a4607@gmail.com' ]# Change to the recipient's email address
    subject = 'Alert your data leaked on dark web'
    body = 'Hello this is from the dark web monitoring bot and please check the site once and see the dashboard page to see the leaked data. Click on the below link to see the leaked data and update them as soon as possible http://127.0.0.1:5000/check_leaks'

    msg = Message(subject=subject, recipients=recipient, body=body)
    try:
        mail.send(msg)
        return 'Email sent successfully!'
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
