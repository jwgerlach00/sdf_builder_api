from flask import Blueprint, render_template, redirect, url_for, request
from . import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user
from flask import session

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username, pw = data['username'], data['password']
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not check_password_hash(user.password, pw):
        # redirect(url_for('auth.login_failed'))
        return 'login_failed', 401
    else:
        login_user(user, remember=True)
        print(current_user.is_active)
        print(current_user.is_authenticated)
        session['username'] = data['username']
        print(session['username'])
        return 'login_success', 204
        # redirect(url_for('auth.get_data'))
    
# @auth.route('/get_data', methods=['GET', 'POST'])
    
@auth.route('/get_data', methods=['GET', 'POST'])
def get_data():
    # help(current_user)
    print(current_user.is_active)
    print(current_user.is_authenticated)
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
