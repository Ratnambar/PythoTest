from flask import Flask,render_template, request, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_login import current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecretkey'


app.secret_key = 'mysecretkey'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'abcd'
app.config['MYSQL_PASSWORD'] = 'abcd1234@#'
app.config['MYSQL_DB'] = 'PythonTest'

# Intialize MySQL
mysql = MySQL(app)



# get registration form
@app.route('/register')
def register():
	return render_template('signup.html')

# get login form
@app.route('/signin',methods=['GET','POST'])
def signin():
	return render_template('login.html')

## get form for adding new address(from lineh <p>Hi, {{ user_id }}</h1> |<a href="/AddAddress/{{user_id }}">Add New Address</a><p> for "index.html")
@app.route('/AddAddress/<int:id>')
def AddAddress(id):
	id = id
	return render_template('addAddress.html',id=id)


# logic for user signup
@app.route('/signup',methods=['POST'])
def signup():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password))
		account = cursor.fetchall()
		if account:
			return "Username is already taken, Please choose another username."
		else:
			cursor.execute('INSERT INTO user (username,password) VALUES (%s, %s)', (username, password,))
			mysql.connection.commit()
			msg = 'You have successfully registered!'
			return render_template('index.html')
	return render_template('signup.html')


# users login code
@app.route('/login', methods=['POST'])
def login():
	msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
		username = request.form['username']
		password = request.form['password']
        # Check if account exists using MySQL
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
		account = cursor.fetchone()
        # If account exists in accounts table in out database
		if account:
			msg = 'Logged in successfully!'
			session['username'] = account['username']
			user_id = account['user_id']
			cursor.execute('SELECT addresses.id,addresses.user_id,addresses.street,addresses.pincode,addresses.country,addresses.state,addresses.phone FROM addresses WHERE addresses.user_id = %s',[user_id])
			addresses = cursor.fetchall()
			addresses = list(addresses)
			return render_template('index.html',user_id=user_id,username=session['username'],addresses=addresses)
		else:
            # Account doesnt exist or username/password incorrect
			msg = 'Incorrect username/password!'
			return msg
    # Show the login form with message (if any)
	return render_template('index.html', msg=msg)


# Save new addresses by handling the update-address.html's form data.
@app.route('/SaveNewAddress/<int:id>',methods=['GET','POST'])
def Add_Address(id):
	id = id
	msg = ''
	if request.method == 'POST':
		user_id = id
		street = request.form['street']
		pincode = request.form['pincode']
		country = request.form['country']
		state = request.form['state']
		phone = request.form['phone']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('INSERT INTO addresses (user_id,street,pincode,country,state,phone) VALUES (%s, %s, %s, %s, %s, %s)', (user_id,street,pincode,country,state,phone))
		mysql.connection.commit()
		msg = 'New Address added successfully!'
		return msg
	return "Address not saved...!"


# render address on which update operation will be performed i.e. update-address page. 
@app.route('/update/<int:id>/<int:user_id>', methods=['GET','POST'])
def Update_Address(id,user_id):
	id = id
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute('SELECT * FROM addresses WHERE id = %s', [id])
	results = cursor.fetchall()
	return render_template('update-address.html', results=list(results))
	return "ok"


# updating and saving the data into database.
@app.route('/ChangeAddress/<int:id>',methods=['GET','POST'])
def Change_Address(id):
	msg = ''
	ids = id
	if request.method == 'POST':
		street = request.form['street']
		pincode = request.form['pincode']
		country = request.form['country']
		state = request.form['state']
		phone = request.form['phone']
		
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('UPDATE addresses SET street=%s, pincode=%s ,country=%s ,state=%s ,phone=%s WHERE id="%s" ', (street,pincode,country,state,phone,ids))
		mysql.connection.commit()	
		msg = "Address changed!..."
		return msg
	return render_template('index.html')







if __name__ == '__main__':
	app.debug=True
	app.run()