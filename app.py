from flask import Flask
from flask_session import Session
from account import authentication
from admin import admin_panel
from main import main_app


app = Flask(__name__)

app.register_blueprint(authentication, url_prefix='')
app.register_blueprint(admin_panel, url_prefix='')
app.register_blueprint(main_app, url_prefix='')
app.config['SECRET_KEY'] = '4fbf27ffdfc1c6c4f5757d507284d960ac0616b0d892ba9e2c424a3c8c867a'
app.config['SESSION_PERMANET'] = False
app.config['SESSION_TYPE'] ='filesystem'
Session(app)
    
if __name__ == '__main__':
     app.run(debug=True)
     
  
    
    