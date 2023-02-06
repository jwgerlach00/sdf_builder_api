from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    # email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


def add_user(db:User, username:str, pw:str) -> None:
    db.session.add(User(username=username, password=generate_password_hash(pw, method='sha256')))
    db.session.commit()

def login(db:User, username:str, pw:str) -> bool:
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, pw):
        return True
    else:
        return False
