from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager, UserMixin
import base64
from flask_session import Session

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    # email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


def create_app():
    app = Flask(__name__)

    # app.config['SECRET_KEY'] = 'secret-key-goes-here'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    # app.config['TESTING'] = False
    # app.config['SESSION_PERMANENT'] = False
    # app.config['SESSION_TYPE'] = 'filesystem'  # Temporary hard-drive storage
    # app.config['SESSION_FILE_THRESHOLD'] = 10
    # Session(app)
    # CORS(app, supports_credentials=True)
    app = Flask(__name__)
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_TYPE'] = 'filesystem'  # Temporary hard-drive storage
    app.config['SESSION_FILE_THRESHOLD'] = 10
    app.secret_key = 'SUKJFIGYRHOWBLUHFFFAOYSANRYYVLZVUVIJVGHUHFFFAOYSAN'  # NaClo-Caffeine
    Session(app)
    CORS(app, supports_credentials=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)
    
    login_manager = LoginManager()
    # login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    login_manager.session_protection = None
    
    # @login_manager.user_loader
    # def load_user(user_id):
    #     # since the user_id is just the primary key of our user table, use it in the query for the user
    #     return User.query.get(int(user_id))
    
    # @login_manager.user_loader
    # def load_user(user_id):
    #     return User.get(user_id)

    
    @login_manager.request_loader
    def load_user_from_request(request):

        # first, try to login using the api_key url arg
        api_key = request.args.get('api_key')
        if api_key:
            user = User.query.filter_by(username=api_key).first()
            if user:
                return user

        # next, try to login using Basic Auth
        api_key = request.headers.get('Authorization')
        if api_key:
            api_key = api_key.replace('Basic ', '', 1)
            try:
                api_key = base64.b64decode(api_key)
            except TypeError:
                pass
            user = User.query.filter_by(username=api_key).first()
            if user:
                return user

        # finally, return None if both methods did not login the user
        return None

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
