from flask import Flask, render_template, redirect, request, jsonify, session, g
from flask_mysqldb import MySQL
import bcrypt
import MySQLdb
app = Flask(__name__)


#----------INITIALIZATION------------#

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mysqlH3lpM3'
app.config['MYSQL_DB'] = 'agnethon'
app.secret_key = 'your_secret_key_here'

# Initialize MySQL
mysql = MySQLdb.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB']
)    #### Changed from original code

#-----------End of Initialization---------#

#---------- CREATE TABLES IN SQL DATABASE-----------------#
cursor=mysql.cursor()
def create_table():
    try:
        with app.app_context():
            # Get the cursor from the MySQL connection
            with mysql.cursor() as cursor:
                # Define the 'users' table schema

                create_events_query = """
                CREATE TABLE IF NOT EXISTS events (
                    name VARCHAR(255) NOT NULL,
                    club VARCHAR(255) NOT NULL,
                    location VARCHAR(512) NOT NULL,
                    date varchar(255),
                    status varchar(255)
                )
                """

                create_student_query = """
                CREATE TABLE IF NOT EXISTS student (
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    password VARCHAR(512) NOT NULL
                )
                """

                create_staff_query="""
                CREATE TABLE IF NOT EXISTS staff (
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    password VARCHAR(512) NOT NULL
                )    
                """

                create_club_query="""
                CREATE TABLE IF NOT EXISTS club (
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    password VARCHAR(512) NOT NULL
                )    
                """
                # Execute the 'CREATE TABLE' statement
                cursor.execute(create_student_query)
                mysql.commit()
                cursor.execute(create_staff_query)
                mysql.commit()
                cursor.execute(create_club_query)
                mysql.commit()
                cursor.execute(create_events_query)
                mysql.commit()
            # Commit the changes
            mysql.commit()
    except MySQLdb.Error as e:
        print(f"Error creating table: {e}")

# Call the 'create_table' function
create_table()

#---------End of create table--------#


#-------CONNECT PAGES-----#
@app.route('/')
def landingpage():
    if 'name' in session:
        return render_template('index.html')
    else:
        return render_template('index.html')
    

@app.route('/homepage')
def homepage():
    if 'name' in session:
        return render_template('homepage.html', name=session['name'])
    else:
        return render_template('homepage.html')
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Fetch user details from the database based on email
        try:
            with mysql.cursor() as cursor:
                cursor.execute("SELECT * FROM student WHERE email = %s", (email,))
                user_data = cursor.fetchone()

            if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data[2].encode('utf-8')):
                # Set the user_id in the session
                session['name'] = user_data[0]
                return redirect('/dashboard')

            elif user_data is None:
                with mysql.cursor() as cursor:
                    cursor.execute("SELECT * FROM club WHERE email = %s", (email,))
                    user_data = cursor.fetchone()
                if user_data is not None:
                    if(password == user_data[2]):
                        # Set the user_id in the session
                        session['name'] = user_data[0]
                        return redirect('/dashboard2')
                
                elif user_data is None:
                    with mysql.cursor() as cursor:
                        cursor.execute("SELECT * FROM staff WHERE email = %s", (email,))
                        user_data = cursor.fetchone()

                    if(password == user_data[2]):
                        # Set the user_id in the session
                        session['name'] = user_data[0]
                        return redirect('/dashboard3')
                
            else:
                return "Invalid email or password. Please try again."
        except MySQLdb.Error as e:
            print(f"Error fetching data: {e}")
            return "An error occurred during login."
    return render_template('login.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        # Get registration details from the form
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']

        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            # Save registration details in the database
            with mysql.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO student (name, email, password) VALUES (%s, %s, %s)",
                    (name, email, hashed_password)
                )
            # Commit the changes
            mysql.commit()

            return redirect('/login')

        except MySQLdb.Error as e:
            print(f"Error inserting data: {e}")
            return "An error occurred during registration."

    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    cursor.execute("SELECT * FROM events")
    data = cursor.fetchall()
    # Render HTML template and pass data to it
    return render_template('indexBen.html', data=data)
    

@app.route('/dashboard2')
def dashboard2():
    if 'name' in session:
        cursor.execute("SELECT * FROM events")
        data = cursor.fetchall()
        # Render HTML template and pass data to it
        return render_template('DASHBOARD 2.html', data=data)

@app.route('/dashboard3')
def dashboard3():
    if 'name' in session:
        cursor.execute("SELECT * FROM events")
        data = cursor.fetchall()
        # Render HTML template and pass data to it
        return render_template('dashboard3.html', data=data) 
    
@app.route('/approval')
def approval():
        cursor.execute("SELECT * FROM events")
        data = cursor.fetchall()
        # Render HTML template and pass data to it
        return render_template('appr.html', data=data)

@app.route('/update_status')
def update_status():
    status = request.form.get('status')
    if status == 'approved':
        # Update status in your SQL table
        cursor.execute("UPDATE events SET status = 'approved' WHERE club = 'Eco club'")
        mysql.commit()
        


@app.route('/addevents', methods=['GET','POST'])
def form():
    if request.method == 'POST':
        # Get registration details from the form
        name = request.form['name']
        club = request.form['club']
        location = request.form['location']
        date = request.form['date']

        

        try:
            # Save registration details in the database
            with mysql.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO events (name, club, location, date) VALUES (%s, %s, %s,%s)",
                    (name, club, location, date)
                )
            # Commit the changes
            mysql.commit()

            return redirect('/dashboard2')

        except MySQLdb.Error as e:
            print(f"Error inserting data: {e}")
            return "An error occurred during registration."

  
    return render_template('form.html')
    
if __name__ == '__main__':
    app.run(debug=True)



