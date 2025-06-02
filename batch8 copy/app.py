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
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'database_name'

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
		return render_template("index.html")
	return redirect(url_for('login'))

@app.route('/check_leaks', methods=['POST'])
def check_leaks():
	if 'loggedin' in session:
		try:
			# Fetch sensitive data patterns from the database
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute("SELECT id,username,password,email,organisation,address,city,state,country,postalcode,employee,phoneno,location FROM accounts")
			sensitive_data_rows = cursor.fetchall()
		except Exception as e:
			return f"Error fetching sensitive data patterns: {str(e)}"
		

		sensitive_data = {}
		for row in sensitive_data_rows:
			if row['id'] ==session['id']:
				data_type = row['id']
				pattern = row['username']
				if data_type not in sensitive_data:
					sensitive_data[data_type] = []
				sensitive_data[data_type].append(pattern)

				data_type = row['id']
				pattern = row['password']
				if data_type not in sensitive_data:
					sensitive_data[data_type] = []
				sensitive_data[data_type].append(pattern)


				data_type = row['id']
				pattern = row['email']
				if data_type not in sensitive_data:
					sensitive_data[data_type] = []
				sensitive_data[data_type].append(pattern)
				

				data_type = row['id']
				pattern = row['organisation']
				if data_type not in sensitive_data:
					sensitive_data[data_type] = []
				sensitive_data[data_type].append(pattern)

				data_type = row['id']
				pattern = row['address']
				if data_type not in sensitive_data:
					sensitive_data[data_type] = []
				sensitive_data[data_type].append(pattern)

				data_type = row['id']
				pattern = row['city']
				if data_type not in sensitive_data:
					sensitive_data[data_type] = []
				sensitive_data[data_type].append(pattern)

				data_type = row['id']
				pattern = row['state']
				if data_type not in sensitive_data:
					sensitive_data[data_type] = []
				sensitive_data[data_type].append(pattern)

				data_type = row['id']
				pattern = row['country']
				if data_type not in sensitive_data:
					sensitive_data[data_type] = []
				sensitive_data[data_type].append(pattern)

				data_type = row['id']
				pattern = row['postalcode']
				if data_type not in sensitive_data:
					sensitive_data[data_type] = []
				sensitive_data[data_type].append(pattern)

				data_type = row['id']
				pattern = row['employee']
				if data_type not in sensitive_data:
					sensitive_data[data_type] = []
				sensitive_data[data_type].append(pattern)

				data_type = row['id']
				pattern = row['phoneno']
				if data_type not in sensitive_data:
					sensitive_data[data_type] = []
				sensitive_data[data_type].append(pattern)

				data_type = row['id']
				pattern = row['location']
				if data_type not in sensitive_data:
					sensitive_data[data_type] = []
				sensitive_data[data_type].append(pattern)

		dark_web_path = os.path.join(os.path.dirname(__file__), 'data', 'dark_web.html')
		if os.path.exists(dark_web_path):
			with open(dark_web_path, 'r', encoding='utf-8') as file:
				html_content = file.read()
			leaked_data = check_for_leaks(html_content, "MyCompany", sensitive_data)
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




if __name__ == '__main__':
    app.run(debug=True)
