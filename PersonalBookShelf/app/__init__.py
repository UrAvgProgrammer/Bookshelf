from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:sw33t890@localhost/books'
engine = sqlalchemy.create_engine('mysql+pymysql://root:sw33t890@localhost')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

import models
from app import controller


