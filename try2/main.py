from flask import Blueprint
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return 'Index'

@main.route('/profile')
def profile():
    return 'Profile'

@main.route('/print_crap', methods=['GET'])
def print_crap():
    # print('ape')
    # print(help(login_manager))
    print('ape')
    return '', 204