import flask
from flask import Flask, session
# from flask_session import Session
from flask_cors import CORS
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import pandas as pd


app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite3'
db = SQLAlchemy(app)
# login_manager = LoginManager()

class SDF(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    smi = db.Column(db.String)
    # activity = db.Column(db.Float, unique=True, nullable=False)
    
    # def __init__(self, smi, activity):
    #     self.smi = smi
    #     self.activity = activity
        
    # def add_col(self, col):
    #     setattr(self, col, db.Column(db.String))
CORS(app, supports_credentials=True)

# with app.app_context():
    
    # )


@app.route('/init_db', methods=['GET'])
def index():
    db.create_all()
    sdf = SDF(smi=['ccc', 'cc'])
    
    db.session.add(sdf)
    db.session.commit()
    print('ape')
    
    for row in db.session.query(SDF, SDF.smi).all():
        print(row.SDF, row.smi)
    
    return '', 204


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=True)