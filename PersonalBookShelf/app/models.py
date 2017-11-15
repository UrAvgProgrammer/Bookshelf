from app import app, mysql




class Bookshelf:

    def __init__(self, title=None, year=None, type=None, author=None, edition=None, isbn=None ,rating=None, raters=None):
        self.title = title
        self.year = year
        self.type = type
        self.author = author
        self.edition = edition
        self.isbn = isbn
        self.rating = rating
        self.raters = raters



    def add(self):
        cursor = mysql.get_db().cursor()

        sql = "INSERT INTO shelf(title,year,type,author,edition,isbn,rating,raters) \
                VALUES('%s','%s','%s','%s','%s','%s','%f','%d')" % \
                (self.title,self.year,self.type,self.author,self.edition, self.isbn, self.rating, self.raters)

        cursor.execute(sql)
        mysql.get_db().commit()


    @staticmethod
    def view():
        cursor = mysql.get_db().cursor()

        sql = "SELECT * from shelf"
        cursor.execute(sql)
        studs = cursor.fetchall()
        return studs

    @staticmethod
    def update(bookid,title,year,type1,author,edition,isbn):
        cursor = mysql.get_db().cursor()

        sql = "UPDATE shelf set title = '%s' where bookid = '%s'" % (title,bookid)
        cursor.execute(sql)
        mysql.get_db().commit()

        sql = "UPDATE shelf set year = '%s' where bookid = '%s'" % (year,bookid)
        cursor.execute(sql)
        mysql.get_db().commit()

        sql = "UPDATE shelf set type = '%s' where bookid = '%s'" % (type1,bookid)
        cursor.execute(sql)
        mysql.get_db().commit()

        sql = "UPDATE shelf set author = '%s' where bookid = '%s'" % (author,bookid)
        cursor.execute(sql)
        mysql.get_db().commit()

        sql = "UPDATE shelf set edition = '%s' where bookid = '%s'" % (edition,bookid)
        cursor.execute(sql)
        mysql.get_db().commit()

        sql = "UPDATE shelf set isbn = '%s' where bookid = '%s'" % (isbn,bookid)
        cursor.execute(sql)
        mysql.get_db().commit()

    @staticmethod
    def db():
        cursor = mysql.get_db().cursor()

        sql = """CREATE DATABASE IF NOT EXISTS books"""
        cursor.execute(sql)
        sql1 = """CREATE TABLE IF NOT EXISTS shelf(
                bookid INT AUTO_INCREMENT NOT NULL,
                title VARCHAR(60) NOT NULL,
                year VARCHAR(60), 
                type VARCHAR(20) NOT NULL,
                author VARCHAR(60) NOT NULL,
                edition VARCHAR(30),
                isbn VARCHAR(60),
                rating float(10),
                raters int(250),
                PRIMARY KEY (bookid))"""
        cursor.execute(sql1)
