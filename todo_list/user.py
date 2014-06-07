from models import User

from flask import Blueprint, request, redirect, render_template ,g
from flask.ext.login import login_user , logout_user , current_user, login_required

# Creating an Index Blueprint in an effort to make the applicaiton Modular
user_blueprint = Blueprint('accounts', __name__)

# Register new user to the app 
@user_blueprint.route('/register' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    user = User(request.form['username'] , request.form['password'])
    user.save() 
    return redirect('/login')

# Login user to the app
@user_blueprint.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    registered_user = User.query.filter_by(username=username,password=password).first()
    
    if registered_user is None:
        return redirect('/login')
    
    login_user(registered_user)
    return redirect('/')

# Logout user from the app
@user_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@user_blueprint.before_request
def before_request():
    g.user = current_user
