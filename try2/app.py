from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager, UserMixin
import base64
from flask_session import Session
from flask import session


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
# app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)
app.secret_key = 'SUKJFIGYRHOWBLUHFFFAOYSANRYYVLZVUVIJVGHUHFFFAOYSAN'  # NaClo-Caffeine
Session(app)
CORS(app, supports_credentials=True, resources={r'/*': {'origins': '*'}})

@app.route('/session_1', methods=['GET', 'POST'])
def session_1():
    # session['save'] = 'test'
    print(session.sid)
    return '', 204

@app.route('/session_2', methods=['GET', 'POST'])
def session_2():
    # print(session['save'])
    print(session.sid)
    return '', 204


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=True)