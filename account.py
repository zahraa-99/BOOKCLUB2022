from flask import Blueprint, render_template, redirect, request, flash, url_for, session
from flask_session import Session
from cs50 import SQL 
from werkzeug.security import generate_password_hash, check_password_hash

authentication = Blueprint('authentication', __name__, static_folder='static', template_folder='templates')

db = SQL('sqlite:///bookclub.db')


@authentication.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    name = request.form.get('name', None)
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    confirm_password = request.form.get('confirm_password', None)
        
    #ensuring all fields must be provided
    if not name or not email or not password:
        flash('You must fill all fields')
        return render_template('register.html')
    
    
    #valdiations for registering new user
    if len(name) < 2 or len(password) < 8:
        flash('Name must be more than 2 characters and password must be more than 8 character')
        return render_template('register.html')
    
    if password != confirm_password:
          flash('Password do not match')
          return render_template('register.html')  
   
    #checking if the user is already registered 
    user = db.execute('SELECT * FROM users WHERE email LIKE ?;', email)
    if len(user) == 1:
        return redirect(url_for('authentication.login'))    
    else:
    #adding user to the database (registering user)
         user_id = db.execute(
            'INSERT INTO users (name, email, password) VALUES (?, ?, ?);',
            name,
            email,
            generate_password_hash(password)
        )
    #redirecting user to the homepage after registering successfully
         session['user_id'] = user_id
         return redirect(url_for('main_app.homepage'))
    
   
 

@authentication.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form.get('email')
    password = request.form.get('password')
    
    #checking if the user is not registered
    user = db.execute('SELECT * FROM users WHERE email LIKE ?;' , email)
    
    if len(user) == 0:
        return redirect(url_for('authentication.register'))

    else:
        if not check_password_hash(user[0]['password'], password):
            flash('Check your login details')
            return render_template('login.html')
        else:
            session['user'] = user
            return redirect(url_for('main_app.homepage'))
          
@authentication.route('/logout') 
def logout():
    Session.clear()
    return redirect(url_for('main_app.homepage'))
      
    
    
if __name__ == '__main__':
     authentication.run(debug=True)
     
