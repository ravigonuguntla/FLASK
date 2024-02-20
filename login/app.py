# Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os  # Add this import
from bs4 import BeautifulSoup


app = Flask(__name__)


app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ravi4613'
app.config['MYSQL_DB'] = 'geeklogin'

mysql = MySQL(app)

def check_for_leaks(html_content, organization_name, sensitive_data):
    soup = BeautifulSoup(html_content, 'html.parser')
    leaked_data = []

    for data_type, patterns in sensitive_data.items():
        for pattern in patterns:
            matches = re.findall(pattern, soup.get_text(), re.IGNORECASE)
            if matches:
                leaked_data.extend(matches)

    return leaked_data


@app.route('/')
def dashboard():
	if 'loggedin' in session:
		return render_template('dashboard.html')
	return redirect(url_for('login'))
    
@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			msg = 'Logged in successfully !'
			return render_template('index.html', msg = msg)
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers !'
		elif not username or not password or not email:
			msg = 'Please fill out the form !'
		else:
			cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)

@app.route("/index")
def index():
	if 'loggedin' in session:
		return render_template("index.html")
	return redirect(url_for('login'))

@app.route('/check_leaks', methods=['POST'])
def check_leaks():
    # Get the absolute path to the dark_web.html file
    dark_web_path = os.path.join(os.path.dirname(__file__), 'data', 'dark_web.html')

    # Check if the file exists before attempting to open it
    if os.path.exists(dark_web_path):
        with open(dark_web_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Define sensitive data patterns to check for in the HTML content
        sensitive_data_patterns = {
            'Names': ["John Doe", "Jane Smith", "Bob Johnson", "Alice Williams"],
            'Emails': [r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'],
            'Phone Numbers': [r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'],
            'Passwords': [r'\bpassword\b', r'\b123456\b', r'\bqwerty\b']
        }

        # Check for leaks in the simulated HTML content
        leaked_data = check_for_leaks(html_content, "MyCompany", sensitive_data_patterns)

        return render_template('dashboard.html', leaked_data=leaked_data)

    else:
        return "Error: dark_web.html file not found."


	
	

@app.route("/display")
def display():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE id = % s',
					(session['id'], ))
		account = cursor.fetchone()
		return render_template("display.html", account=account)
	return redirect(url_for('login'))


@app.route("/update", methods=['GET', 'POST'])
def update():
	msg = ''
	if 'loggedin' in session:
		if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
			username = request.form['username']
			password = request.form['password']
			email = request.form['email']
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute(
				'SELECT * FROM accounts WHERE username = % s',
					(username, ))
			account = cursor.fetchone()
			if account:
				msg = 'Account already exists !'
			elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
				msg = 'Invalid email address !'
			elif not re.match(r'[A-Za-z0-9]+', username):
				msg = 'name must contain only characters and numbers !'
			else:
				cursor.execute('UPDATE accounts SET username =% s,\
				password =% s, email =% s,WHERE id =% s', (
					username, password, email
				(session['id'], ), ))
				mysql.connection.commit()
				msg = 'You have successfully updated !'
		elif request.method == 'POST':
			msg = 'Please fill out the form !'
		return render_template("update.html", msg=msg)
	return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)