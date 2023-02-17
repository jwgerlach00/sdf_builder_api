from flask import Blueprint, request
from flask_login import login_required, current_user
from flask import session

from db import db


main = Blueprint('main', __name__)


@main.route('/session_1', methods=['GET', 'POST'])
def session_1():
    session['save'] = 'test'
    print(session.sid)
    return '', 204

@main.route('/session_2', methods=['GET', 'POST'])
def session_2():
    print(session['save'])
    print(session.sid)
    return '', 204

@main.route('/add_mol_to_table', methods=['POST'])
@login_required
def add_mol_to_table():
    print(current_user.username)
    data = request.get_json()
    smi = data['smi']

    # db.add_entry()
    return '', 204
    


    
# @login_manager.request_loader
# def load_user_from_request(request):

#     # first, try to login using the api_key url arg
#     api_key = request.args.get('api_key')
#     if api_key:
#         user = User.query.filter_by(username=api_key).first()
#         if user:
#             return user

#     # next, try to login using Basic Auth
#     api_key = request.headers.get('Authorization')
#     if api_key:
#         api_key = api_key.replace('Basic ', '', 1)
#         try:
#             api_key = base64.b64decode(api_key)
#         except TypeError:
#             pass
#         user = User.query.filter_by(username=api_key).first()
#         if user:
#             return user

#     # finally, return None if both methods did not login the user
#     return None

# blueprint for auth routes in our app
# from .auth import auth as auth_blueprint

# blueprint for non-auth parts of app
# from .main import main as main_blueprint
# app.register_blueprint(main_blueprint)

# return app
