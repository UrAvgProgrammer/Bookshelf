from flask import Flask, render_template, request, flash, redirect, url_for, session
import models
from forms import Forms, BookForms
from app import app, mysql
from wtforms import Form, StringField, TextAreaField, PasswordField, validators




@app.route('/' , methods = ['POST', 'GET'])
def index():
    models.Bookshelf.db()
    studs = models.Bookshelf.view()
    if request.method == 'POST':
        cursor = mysql.get_db().cursor()
        ratingNew = int(request.form['rate'])
        bookidNew = request.form['Store']

        sql = "SELECT rating FROM shelf WHERE bookid = '%s'" % (bookidNew,)
        cursor.execute(sql)
        for i in cursor.fetchall():
            rate = float(i[0])

        sql = "SELECT raters FROM shelf WHERE bookid = '%s'" % (bookidNew,)
        cursor.execute(sql)
        for j in cursor.fetchall():
            raters = int(j[0])

        dividend = ratingNew+rate
        ratersTot = raters+1

        total = float(dividend/ratersTot)

        sql = "UPDATE shelf set rating = '%f' where bookid = '%s'" % (total,bookidNew)
        cursor.execute(sql)
        mysql.get_db().commit()

        sql = "UPDATE shelf set raters = '%d' where bookid = '%s'" % (ratersTot,bookidNew)
        cursor.execute(sql)
        mysql.get_db().commit()

        studs = models.Bookshelf.view()
        return render_template("personalshelf.html",studs = studs)

    else:
        return render_template("personalshelf.html",studs = studs)


@app.route('/adder', methods = ['POST', 'GET'])
def adder():

    form = Forms(request.form)
    if request.method == 'POST':
        titleNew = form.titleNew.data
        yearNew = form.yearNew.data
        typeNew = form.typeNew.data
        authorNew = form.authorNew.data
        editionNew = form.editionNew.data
        isbnNew = form.isbnNew.data

        if form.validate():
            book = models.Bookshelf(title = titleNew, year = yearNew, type = typeNew , author = authorNew, edition = editionNew, isbn = isbnNew, rating = 0, raters = 0)
            book.add()
            flash('Book successfully added', 'success')
            return render_template("add.html", form=form)

        elif not form.validate():
            flash("Please don't leave any blank", 'error')
            return render_template("add.html", form=form)
        else:
            return render_template("add.html", form=form)


    else:
        return render_template("personalshelf.html", form=form)

@app.route('/view')
def view():

    studs = models.Bookshelf.view()
    return render_template("personalshelf.html",studs = studs)

@app.route('/delete', methods = ['POST', 'GET'])
def deletefunc():
    deleteStore = request.form['Store']
    studs = models.Bookshelf.view()
    if request.method == 'POST':
        cursor = mysql.get_db().cursor()

        sql = "DELETE from shelf where bookid = '%s' " % (deleteStore,)
        cursor.execute(sql)
        mysql.get_db().commit()
        studs = models.Bookshelf.view()
        flash('Book Successfully deleted', 'success')
        return render_template("personalshelf.html",studs = studs)

    else:
        return render_template("personalshelf.html",studs = studs)

@app.route('/updateBook', methods = ['POST', 'GET'])
def updateGet():
    updateStore = request.form['Store']
    studs = models.Bookshelf.view()
    if request.method == 'POST':

        session['bookidNew'] = updateStore
        return redirect(url_for('update'))

    else:
        return render_template("personalshelf.html",studs = studs)

@app.route('/updateForm', methods = ['POST', 'GET'])
def update():

    form = Forms(request.form)
    bookidNew = session['bookidNew']
    if request.method == 'POST':
        titleNew = form.titleNew.data
        yearNew = form.yearNew.data
        typeNew = form.typeNew.data
        authorNew = form.authorNew.data
        editionNew = form.editionNew.data
        isbnNew = form.isbnNew.data


        if form.validate():
            models.Bookshelf.update(bookidNew,titleNew,yearNew,typeNew,authorNew,editionNew,isbnNew)
            flash('Successfully Updated', 'success')
            return render_template("update.html", form = form)
        elif not form.validate():
                flash('Please fill up each of the following', 'error')
                return render_template("update.html", form = form)

        else:
            flash('error in update operation', 'error')
            return render_template("updateGet.html", form=form)


    else:
        return render_template("update.html", form=form)


@app.route('/searchGet', methods = ['POST', 'GET'])
def searchGet():
    studs = models.Bookshelf.view()
    search = request.form['search']
    if request.method == 'POST':
        cursor = mysql.get_db().cursor()
        search1 = "%"+search+"%"


        sql = "SELECT * FROM shelf WHERE title LIKE '%s' or year LIKE '%s' or type LIKE '%s' or author LIKE '%s' or edition LIKE '%s' or isbn LIKE '%s'" % (search1,search1,search1,search1,search1,search1)
        cursor.execute(sql)
        studs = cursor.fetchall()

        if studs is None:
            flash('Book ot in record or Letter capitalization incorrect', 'error')
            return render_template("personalshelf.html",studs = studs)

        else:


            return render_template("personalshelf.html",studs = studs)


    else:
        return render_template("studentDatabase.html")


