from flask import Flask, render_template, request, flash, redirect, url_for, session
from models import *
from forms import Forms, BookForms
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from app import app, db


@app.route('/', methods = ['POST', 'GET'])
def index():
    db.create_all()
    studs = Shelf.query.all()

    if request.method == 'POST':
        ratingNew = int(request.form['rate'])
        bookidNew = request.form['Store']



        userRate = Shelf.query.filter_by(bookid=bookidNew).first()
        rate = userRate.rating
        raters = userRate.raters

        dividend = ratingNew+rate
        ratersTot = raters+1

        total = float(dividend/ratersTot)

        userRate.rating = total
        userRate.raters = ratersTot
        db.session.commit()

        studs = Shelf.query.all()
        return render_template("personalshelf.html", studs=studs)

    else:
        return render_template("personalshelf.html", studs=studs)


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
            book = Shelf(titleNew,yearNew,typeNew,authorNew,editionNew,isbnNew,0,0)
            db.session.add(book)
            db.session.commit()
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

    studs = Shelf.query.all()
    return render_template("personalshelf.html",studs = studs)


@app.route('/delete', methods = ['POST', 'GET'])
def deletefunc():
    deleteStore = request.form['Store']
    studs = Shelf.query.all()
    if request.method == 'POST':
        Shelf.query.filter_by(bookid=deleteStore).delete()
        db.session.commit()
        studs = Shelf.query.all()
        flash('Book Successfully deleted', 'success')
        return render_template("personalshelf.html",studs = studs)

    else:
        return render_template("personalshelf.html",studs = studs)

@app.route('/updateBook', methods = ['POST', 'GET'])
def updateGet():
    updateStore = request.form['Store']
    studs = Shelf.query.all()
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
            updateNew = Shelf.query.filter_by(bookid = bookidNew).first()

            updateNew.title = titleNew
            updateNew.year = yearNew
            updateNew.type = typeNew
            updateNew.author = authorNew
            updateNew.edition = editionNew
            updateNew.isbn = isbnNew
            db.session.commit()



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
    studs = Shelf.query.all()
    search = request.form['search']
    if request.method == 'POST':
        search1 = "%"+search+"%"
        studs = Shelf.query.filter((Shelf.title.like(search1)) | (Shelf.year.like(search1)) |
                                  (Shelf.type.like(search1)) | (Shelf.author.like(search1)) |
                                  (Shelf.edition.like(search1)) | (Shelf.isbn.like(search1)) | (Shelf.rating.like(search1)))

        return render_template("personalshelf.html",studs = studs)

    else:
        return render_template("personalshelf.html",studs = studs)




