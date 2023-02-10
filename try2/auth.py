from flask import Blueprint, render_template, redirect, url_for, request
from . import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from flask import session

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username, pw = data['username'], data['password']
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not check_password_hash(user.password, pw):
        return 'login_failed', 401
    else:
        print(current_user.is_active)
        print(current_user.is_authenticated)
        login_user(user, remember=False)
        print(current_user.is_active)
        print(current_user.is_authenticated)
        print(current_user.username)
        session['username'] = data['username']
        # session['user'] = current_user
        print(session['username'])
        return 'login_success', 204
    
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return 'logout_success', 204
    
@auth.route('/get_data', methods=['GET'])
def get_data():
    # help(current_user)
    print(current_user.is_active)
    print(current_user.is_authenticated)
    # print(current_user.username)
    print(session['username'])
    return 'abc'
    
    # return ('login_success', 204) if login(db, username, pw) else ('login_failed', 401)
    
@auth.route('/login_failed', methods=['GET'])
def login_failed():
    return 'login_failed', 401

@auth.route('/exists', methods=['GET'])
def exists():
    return 'user_exists', 409

def add_user(db:User, username:str, pw:str) -> None:
    db.session.add(User(username=username, password=generate_password_hash(pw, method='sha256')))
    db.session.commit()

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username, pw = data['username'], data['password']

    if User.query.filter_by(username=username).first():
        return redirect(url_for('auth.exists'))
    else:
        add_user(db, username, pw)

    return 'register_success', 204

@auth.route('/is_authenticated', methods=['GET'])
def is_authenticated():
    return ('yes', 204) if current_user.is_authenticated else ('no', 401)
