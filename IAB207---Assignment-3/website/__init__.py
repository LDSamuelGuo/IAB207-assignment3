# import flask - from the package import class
from flask import Flask, render_template
from flask_bootstrap import Bootstrap4

from flask_sqlalchemy import SQLAlchemy
from flask_wtf import *
from werkzeug.utils import *
from flask_login import LoginManager

db = SQLAlchemy()
app = Flask(__name__, template_folder='./templates')
# create a function that creates a web application
# a web server will run this web application


def create_app():

    # this is the name of the module/package that is calling this app
    
    app.debug = True
    app.secret_key = 'utroutoru'

    # set the app configuration data
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sitedata.sqlite'

    # initialize db with flask app
    db.init_app(app)

    bootstrap = Bootstrap4(app)

    # initialize the login manager
    login_manager = LoginManager()

    # set the name of the login function that lets user login
    # in our case it is auth.login (blueprintname.viewfunction name)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'You Must Login to Access This Page!'
    login_manager.login_message_category = 'list-group-item-danger'
    login_manager.init_app(app)

    # create a user loader function takes userid and returns User
    from .models import user  # importing here to avoid circular references

    @login_manager.user_loader
    def load_user(user_id):
        from .models import user
        return user.query.get(int(user_id))

    # Allow image uploads
    UPLOAD_FOLDER = '/static/image'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

   # importing views module here to avoid circular references
    # a commonly used practice.
    from . import views
    app.register_blueprint(views.main)

    from . import auth
    app.register_blueprint(auth.authBP)

    return app

@app.errorhandler(404) 

def not_found(e): 
 return render_template("404.html")

@app.errorhandler(500) 
# inbuilt function which takes error as parameter 
def not_found(e): 
  return render_template("500.html")
