from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash


class Users(UserMixin, db.Model):
    __tablename__ = 'usersdatabase'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    contact_number = db.Column(db.String(11))
    sex = db.Column(db.CHAR(1), nullable=False)
    birth_date = db.Column(db.DATE, nullable=False)

    def __init__(self, username='', password='', first_name='', last_name='', contact_number='', sex='', birth_date=''):
        self.username = username
        self.password = generate_password_hash(password, method='sha256')
        self.first_name = first_name
        self.last_name = last_name
        self.contact_number = contact_number
        self.sex = sex
        self.birth_date = birth_date


class Books(db.Model):
    __tablename__ = 'books'
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(20))
    types = db.Column(db.String(20))
    author = db.Column(db.String(60))
    edition = db.Column(db.String(20))
    isbn = db.Column(db.String(30))
    rating = db.Column(db.Float(20))
    raters = db.Column(db.Float(20))

    def __init__(self, title='', year='', types='', author='', edition='', isbn='', rating='', raters=''):
        self.title = title
        self.year = year
        self.type = types
        self.author = author
        self.edition = edition
        self.isbn = isbn
        self.rating = rating
        self.raters = raters
