from flask import Flask
from app import db, app



class Shelf(db.Model):
    __tablename__ = 'shelf'
    bookid = db.Column('bookid', db.Integer, primary_key=True)
    title = db.Column('title', db.String(60))
    year = db.Column('year', db.String(20))
    type = db.Column('type', db.String(20))
    author = db.Column('author', db.String(60))
    edition = db.Column('edition', db.String(20))
    isbn = db.Column('isbn', db.String(30))
    rating = db.Column('rating', db.Float(20))
    raters = db.Column('raters', db.Float(20))


    def __init__(self, title='', year='', type='', author='', edition='', isbn='',rating='', raters=''):
        self.title = title
        self.year = year
        self.type = type
        self.author = author
        self.edition = edition
        self.isbn = isbn
        self.rating = rating
        self.raters = raters



