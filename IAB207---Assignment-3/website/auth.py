from flask import (
    Blueprint, flash, render_template, request, url_for, redirect
)
import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from werkzeug.security import generate_password_hash, check_password_hash
from .models import *
from .forms import LoginForm, RegisterForm
from flask_login import login_user, login_required, logout_user
from . import db


# create a blueprint
authBP = Blueprint('auth', __name__, url_prefix='/auth')


@authBP.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.is_submitted():
        print('In Login View function')
        error = None
        if(form.validate_on_submit() == True):
            user_name = form.user_name.data
            password = form.password.data
            u1 = user.query.filter_by(user_name=user_name).first()
            if u1 is None:
                error = 'Incorrect user name'
            # takes the hash and password
            elif not check_password_hash(u1.password_hash, password):
                error = 'Incorrect password'

            if error is None:
                login_user(u1)
                # this gives the url from where the login page was accessed
                nextp = request.args.get('next')
                print(nextp)
                if nextp is None or not nextp.startswith('/'):
                    return redirect(url_for('main.index'))
                return redirect(nextp)
            else:
                flash(error, 'list-group-item-danger')
        return render_template('loginSignUp.html', form=form, pageType=request.path)
    return render_template('loginSignUp.html', form=form, pageType=request.path)


@authBP.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm()

    if form.is_submitted():
        print('test1')
        # Assign form details to new user fields
        newUser = user()

        # get password data before hashing
        password = form.confirm.data
        password_hash = generate_password_hash(password)
        print(password_hash)

        newUser.user_name = form.user_name.data
        newUser.email_id = form.email_id.data
        newUser.password_hash = password_hash
        newUser.address = form.address.data
        newUser.contact = form.contact.data

        # For checking passwords match
        password = form.password.data
        passwordCheck = form.confirm.data

        # Check user doesn't already exist and proceed
        if checkExists(newUser.user_name, user) == False:
            print('test2')
            # Check passwords match
            if password == passwordCheck:
                print(newUser.user_name)
                db.session.add(newUser)
                db.session.commit()
                flash("You've successfully registered!",
                      'list-group-item-success')
                return render_template('loginSignUp.html', form=form, pageType=request.path)
            else:
                print('test3')
                flash("Your passwords need to match",
                      'list-group-item-danger')
        # Return error
        elif checkExists(newUser.user_name, user) == True:
            print(True)
            error = 'Username already exists'
            flash(error, 'list-group-item-danger')

    return render_template('loginSignUp.html', form=form, pageType=request.path)

# Temp for testing while waiting for Isaacs version


@authBP.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@authBP.route('/accountInformation')
def accountInformation():

    return render_template('accountInformation.html')


def checkFile(form):
    print("test")
    # Get uploaded image from form
    img = form.image.data

    # Pull filename to check
    filename = img.filename

    # Get base file path (this files location)
    Base = os.path.dirname(__file__)

    # Join this files location with the image file and the location to store it
    uploadPath = os.path.join(Base, 'static/img', secure_filename(filename))

    img.save(uploadPath)


def checkExists(nameToCheck, table):
    test2 = table.query.all()
    print(test2)
    test = None
    print('testCheck')
    if table == user:
        print('testCheckUsers')
        if test2 == []:
            test = False
        for users in test2:
            if users.user_name == nameToCheck:
                print('testCheckReturnT')
                return True
            else:
                print('testCheckReturnF')
                test = False
        if test == False:
            return test
    elif table == event:
        for events in test2:
            if events.eventName == nameToCheck:
                return True
            else:
                test = False
        if test == False:
            return test


def checkTicketsAvailable(ticketsBought, table):
    test2 = table.query.all()
    test = None
    if table == event:
        for events in test2:
            if events.tickets >= ticketsBought:
                return True
            else:
                return False
