from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///university/tmp/test.db'
app.secret_key = 'some_random_key'
db = SQLAlchemy(app)

from my_app.university.views import university
app.register_blueprint(university)

db.create_all()