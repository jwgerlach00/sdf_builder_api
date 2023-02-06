from database import conn, cursor, create_table, db_2_df
import pandas as pd
from flask import Flask, request
import flask_login
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


user_id = 'jwgerlach00'

app = Flask(__name__)
db = SQLAlchemy(app)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sql.db'
app.secret_key = 'thisisasupersecretkey'
CORS(app, supports_credentials=True)



# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
#     username = db.Column(db.String(100))
#     password = db.Column(db.String(100))
    


users = {
    'jacob': {'password': 'password'}
}
login_manager = flask_login.LoginManager()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(80), nullable=False)

@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return

    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.json.get('username')
    if username not in users:
        return

    user = User()
    user.id = username
    return user

@login_manager.unauthorized_handler
def unauthorized_callback():
    print('unauth')
    return '', 204

login_manager.init_app(app)


# create_table(name=user_id)
# cursor.execute(f"INSERT INTO {user_id} VALUES (2, 'ccc')")
# conn.commit()

# records = cursor.execute(f"SELECT * FROM {user_id}")
# print(records)
# for row in records:
#     print(row)

# out = db_2_df(name=user_id)
# print(out)

# @app.route('/create_table', methods=['GET'])
# def create_table():
#     create_table(name=user_id)
#     return '', 204

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username, pw = data['username'], data['password']
        
         
        if username in users and users[username]['password'] == pw:
            user = User()
            user.id = username
            flask_login.login_user(user)
            return '', 204
        else:
            return '', 401
        # return '', 204


@app.route('/print_crap', methods=['GET'])
@flask_login.login_required
def print_crap():
    # print('ape')
    # print(help(login_manager))
    return '', 204
    
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username, pw = data['username'], data['password']
        
        return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=True)