from try2 import db, create_app
# db.create_all(app=create_app()) # pass the create_app result so Flask-SQLAlchemy gets the configuration.
# help(db.create_all)
with create_app().app_context():
    db.create_all()