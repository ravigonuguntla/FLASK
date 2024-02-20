# Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
import MySQLdb.cursors
import re
import os  # Add this import
from bs4 import BeautifulSoup

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
			return render_template('dashboard.html')
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'postalcode' in request.form and 'organisation' in request.form and 'employee' in request.form and 'phoneno' in request.form and 'location' in request.form :
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		organisation = request.form['organisation']
		address = request.form['address']
		city = request.form['city']
		state = request.form['state']
		country = request.form['country']
		postalcode = request.form['postalcode']
		employee = request.form['employee']
		phoneno= request.form['phoneno']
		location = request.form['location']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(
            'SELECT * FROM accounts WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'name must contain only characters and numbers !'
		else:
			cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s)',(username, password, email, organisation, address, city,state, country, postalcode, employee ,phoneno , location))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg=msg)

@app.route("/index")
def index():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT organisation FROM accounts WHERE id = % s',
					(session['id'], ))
		account = cursor.fetchone()
		return render_template("index.html",account = account)
	return redirect(url_for('login'))

@app.route('/check_leaks', methods=['POST'])
def check_leaks():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    try:
        # Fetch sensitive data patterns from the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT id, username, password, email, organisation, address, city, state, country, postalcode, employee, phoneno, location FROM accounts")
        sensitive_data_rows = cursor.fetchall()
    except Exception as e:
        return f"Error fetching sensitive data patterns: {str(e)}"
    sensitive_data = {}
    for row in sensitive_data_rows:
        if row['id'] == session['id']:
            data_type = row['id']
            for key in ['username', 'password', 'email', 'organisation', 'address', 'city', 'state', 'country', 'postalcode', 'employee', 'phoneno', 'location']:
                pattern = row[key]
                sensitive_data.setdefault(data_type, []).append(pattern)
    dark_web_path = os.path.join(os.path.dirname(__file__), 'data', 'dark_web.html')
    if os.path.exists(dark_web_path):
        with open(dark_web_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        leaked_data = check_for_leaks(html_content, "my company" ,sensitive_data)
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
		if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'postalcode' in request.form and 'organisation' in request.form and 'employee' in request.form and 'phoneno' in request.form and 'location' in request.form:
			username = request.form['username']
			password = request.form['password']
			email = request.form['email']
			organisation = request.form['organisation']
			address = request.form['address']
			city = request.form['city']
			state = request.form['state']
			country = request.form['country']
			postalcode = request.form['postalcode']
			employee = request.form['employee']
			phoneno= request.form['phoneno']
			location = request.form['location']
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
				password =% s, email =% s, organisation =% s, \
				address =% s, city =% s, state =% s, \
				country =% s, postalcode =% s,employee =% s ,phoneno= % s, location =% s WHERE id =% s', (username, password, email, organisation,address, city, state, country, postalcode, employee,phoneno,location , (session['id'], ), ))
				mysql.connection.commit()
				msg = 'You have successfully updated !'
		elif request.method == 'POST':
			msg = 'Please fill out the form !'
		return render_template("update.html", msg=msg)
	return redirect(url_for('login'))

@app.route('/admin/dashboard')
def admin_dashboard():
	if 'admin_logged_in' not in session:
		return redirect('/admin/login')
	if request.method == 'GET' and 'check_users' in request.args:
		cur = mysql.connection.cursor()
		cur.execute("SELECT username,organisation,email FROM accounts")
		users = cur.fetchall()
		cur.close()
		return render_template('admin_dashboard.html', users=users)
	return render_template('admin_dashboard.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']       
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (username, password))
        admin = cur.fetchone()
        cur.close()
        if admin:
            session['admin_logged_in'] = True
            return redirect('/admin/dashboard')
        else:
            return 'Invalid username or password'   
    return render_template('admin_login.html')


@app.route('/admin/view_users')
def admin_view_users():
    if 'admin_logged_in' not in session:
        return redirect('/admin/login')
    cur = mysql.connection.cursor()
    cur.execute("SELECT username,organisation,email FROM accounts")
    users = cur.fetchall()
    cur.close()
    return render_template('admin_dashboard.html', users=users)

@app.route('/admin/monitor')
def admin_monitor():
	if 'admin_logged_in' not in session:
		return redirect('/admin/login')
	if request.method == 'GET' and 'check_users' in request.args:
		cur = mysql.connection.cursor()
		cur.execute("SELECT username,organisation,email FROM accounts")
		users = cur.fetchall()
		cur.close()
		return render_template('admin_monitor.html', users=users )
	return render_template('admin_monitor.html') 

@app.route('/admin/monitor_data')
def admin_monitor_data():
    if 'admin_logged_in' not in session:
        return redirect('/admin/login')  
    cur = mysql.connection.cursor()
    cur.execute("SELECT username,organisation,email,id FROM accounts")
    users = cur.fetchall()
    cur.close()
    return render_template('admin_monitor.html', users=users)

@app.route('/send_email')
def send_email():
	viewid = request.args.get('id')
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cur.execute("SELECT email FROM accounts where id = % s",(viewid, ))
	users = cur.fetchone()
	cur.close()
	if users:
		recipient = users['email']
	else:
		return 'User not found'
	subject = 'Alert your data leaked on dark web'
	body = 'Hello this is from the dark web monitoring bot and please check the site once and see the dashboard page to see the leaked data. Click on the below link to see the leaked data and update them as soon as possible http://127.0.0.1:5000/check_leaks'
	msg = Message(subject=subject, recipients=[recipient], body=body)   
	try:
		mail.send(msg)
		return 'Email sent successfully!'
	except Exception as e:
		return str(e)
   
@app.route('/admin/check_leaks', methods=['POST','GET'])
def admin_check_leaks():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    try:
        viewid = request.args.get('id')
        # Fetch sensitive data patterns from the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT id, username, password, email, organisation, address, city, state, country, postalcode, employee, phoneno, location FROM accounts where id = % s",(viewid,))
        sensitive_data_rows = cursor.fetchone()
    except Exception as e:
        return f"Error fetching sensitive data patterns: {str(e)}"
    if sensitive_data_rows:
        sensitive_data = {}
        data_type = sensitive_data_rows['id']
        for key in ['username', 'password', 'email', 'organisation', 'address', 'city', 'state', 'country', 'postalcode', 'employee', 'phoneno', 'location']:
            pattern = sensitive_data_rows[key]
            sensitive_data.setdefault(data_type, []).append(pattern)
    dark_web_path = os.path.join(os.path.dirname(__file__), 'data', 'dark_web.html')
    if os.path.exists(dark_web_path):
        with open(dark_web_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        leaked_data = check_for_leaks(html_content, "my company" ,sensitive_data)
        return render_template('admin_monitor.html', leaked_data=leaked_data)
    else:
        return "Error: dark_web.html file not found."


if __name__ == '__main__':
    app.run(debug=True)