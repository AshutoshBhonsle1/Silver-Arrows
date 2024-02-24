from flask import Flask, render_template, redirect, request, session, g
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
mysql = MySQL(app)    #### Changed from original code


@app.route('/')
def landingpage():
    if 'name' in session:
        return render_template('index.html')
    else:
        return render_template('index.html')
    
@app.route('/login')
def login():
    return render_template('loginSAM.html')

@app.route('/homepage')
def homepage():
    if 'name' in session:
        return render_template('homepage.html', name=session['name'])
    else:
        return render_template('homepage.html')
    
@app.route('/dashboard')
def dashboard():
    if 'name' in session:
        return render_template('indexBen.html', name=session['name'])
    else:
        return render_template('indexBen.html')
    

@app.route('/dashboard2')
def dashboard2():
    if 'name' in session:
        return render_template('DASHBOARD2.html', name=session['name'])
    else:
        return render_template('DASHBOARD2.html')    

@app.route('/form')
def form():
    if 'name' in session:
        return render_template('form.html')
    
if __name__ == '__main__':
    app.run(debug=True)
