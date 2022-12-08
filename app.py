from flask import Flask, render_template, request, redirect, flash, url_for
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from cs50 import SQL

app = Flask(__name__)

db = SQL('sqlite:///')
app.config['SECRET_KEY'] = '4fbf27ffdfc1c6c4f5757d507284d960ac0616b0d892ba9e2c424a3c8c867a'
app.config['SESSION_PERMANET'] = False
app.config['SESSION_TYPE'] ='filesystem'
Session(app)


@app.route('/')
def homepage():
   return render_template('homepage.html')

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    name = request.form.get('name')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
        
    #ensuring all fields must be provided
    if not name or not username or not email or not password:
        flash('You must fill all fields')
        return render_template('register.html', error=True) 
            
    #valdiations
    if len(name) < 2:
        flash('Name must be more than one character') 
    elif len(username) < 8:
          flash('Username must be more than 8 characters')
    elif len(password) < 8:
          flash('Password must be more than 8 characters')
    elif password != confirm_password:
          flash('Password do not match')
          return render_template('register.html', error=True)
            
        #checking if the user is already registered 
    users = db.execute('SELECT * FROM usres WHERE email LIKE ?;' , email)
    if len(users) == 1:
            flash('Email address is already registered')
            return render_template('register.html', error=True)
        
        #adding user to the database (registering user)
    user_id = db.execute(
            'INSERT INTO users (name, username, email, password) VALUES (?, ?, ?, ?);',
            name,
            username,
            email,
            generate_password_hash(password)
        )
    
    Session['user_id'] = users[0]['id']
    
    #redirecting user to the homepage 
    return redirect(url_for('homepage'))

@app.route('/login')
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    
if __name__ == '__main__':
     app.run(debug = True)
     
  
    
    