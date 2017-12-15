from flask import Flask, render_template, flash, url_for, redirect
from forms import *
from models import *
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from app import app, db
from flask import Flask, render_template, request, flash, redirect, url_for, session
from forms import Forms

app.secret_key = '31498657699432922335'
app.debug = True
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def index():
    if current_user.is_authenticated is True:
        return redirect(url_for('home'))
    return render_template('index.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated is True:
        return redirect(url_for('home'))
    elif form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=True)
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password')
                return render_template('login.html', form=form)
        else:
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if current_user.is_authenticated is True:
        return redirect(url_for('home'))
    elif form.validate_on_submit():
        hashed = generate_password_hash(form.password.data, method='sha256')
        new_user = User(form.username.data, hashed, form.first_name.data,
                         form.last_name.data, form.contact.data,
                         form.year.data+'-'+form.month.data+'-'+form.day.data,form.sex.data)
        db.session.add(new_user)
        db.session.commit()
        bookshelf = Bookshelf(new_user.id,new_user.id)
        db.session.add(bookshelf)
        db.session.commit()
        login_user(new_user, remember=True)
        return redirect(url_for('home'))
    return render_template('registration.html', form=form)


@app.route('/home')
@login_required
def home():
    return render_template('dashboard.html', name=current_user)


@app.route('/profile/<int:user_id>/<int:page_num>', methods=['GET', 'POST'])
@login_required
def profile(user_id,page_num):
    session['page'] = page_num
    session['forpage'] = 1
    comments = UserComment.query.filter(UserComment.userCommentee == user_id).paginate(page_num,10)

    a=[]
    b=[]
    for s in comments.items:
        s = User.query.filter_by(id=s.userCommenter).first()
        a.append(s.first_name)
        b.append(s.last_name)


    if user_id == current_user.id:

        pags = ContainsAsscociation.query.filter(ContainsAsscociation.shelf_id == current_user.id).paginate(page_num,6)

        x=[]
        y=[]
        for p in pags.items:
            s = WrittenByAssociation.query.filter_by(book_id=p.book_id).first()
            author = Author.query.filter_by(author_id=s.author_id).first()
            x.append(author.author_first_name)
            y.append(author.author_last_name)


        form = EditProfile()
        if form.validate_on_submit():
            update = User.query.filter_by(id=current_user.id).first()
            update.first_name = form.first_name.data
            update.last_name = form.last_name.data
            update.contact_number = form.contact.data
            db.session.commit()
            return redirect(url_for('home'))


    elif user_id != current_user:
        pags = ContainsAsscociation.query.filter(ContainsAsscociation.shelf_id == user_id).paginate(page_num,6)
        form = User.query.filter(User.id == user_id).first()
        formComment = CommentForms(request.form)


        x=[]
        y=[]
        for p in pags.items:
            s = WrittenByAssociation.query.filter_by(book_id=p.book_id).first()
            author = Author.query.filter_by(author_id=s.author_id).first()
            x.append(author.author_first_name)
            y.append(author.author_last_name)



        return render_template('diffuser.html', pags = pags, data=current_user,form = form, x=x, y=y, comments=comments, formComment=formComment,a=a,b=b)

    return render_template('profile.html', data=current_user, form=form, pags = pags, x=x, y=y)

@app.route('/adder', methods = ['POST', 'GET'])
@login_required
def adder():
    form = Forms(request.form)
    if request.method == 'POST':
        titleNew = form.titleNew.data
        yearNew = form.yearNew.data
        typeNew = form.typeNew.data
        editionNew = form.editionNew.data
        isbnNew = form.isbnNew.data
        publisherNew = form.publisher_id.data
        authorFirstNew = form.authorFirstNew.data
        authorLastNew = form.authorLastNew.data

        pub = '%'+str(publisherNew)+'%'
        if form.validate():
            books = Books.query.filter((Books.title == titleNew) & (Books.edition == editionNew) & (Books.year_published == yearNew) & (Books.isbn == isbnNew)).first()
            publishers = Publisher.query.filter((Publisher.publisher_name.like(pub))).first()
            author = Author.query.filter((Author.author_first_name == authorFirstNew) & (Author.author_last_name == authorLastNew)).first()


            if (books is None) or (publishers is None) or (author is None):
                if publishers is None:
                    pubbook = Publisher(publisherNew)
                    db.session.add(pubbook)
                    db.session.commit()
                    pub_id = Publisher.query.filter((Publisher.publisher_name == publisherNew)).first()
                    if author is None:
                        authbook = Author(authorFirstNew,authorLastNew)
                        db.session.add(authbook)
                        db.session.commit()
                    elif author is not None:
                        auth_id = Author.query.filter((Author.author_first_name == authorFirstNew) and (Author.author_last_name == authorLastNew)).first()


                elif publishers is not None:
                    pub_id = Publisher.query.filter((Publisher.publisher_name == publisherNew)).first()
                    if author is None:
                        authbook = Author(authorFirstNew,authorLastNew)
                        db.session.add(authbook)
                        db.session.commit()
                    elif author is not None:
                        auth_id = Author.query.filter((Author.author_first_name == authorFirstNew) and (Author.author_last_name == authorLastNew)).first()


                auth_id = Author.query.filter((Author.author_first_name == authorFirstNew) and (Author.author_last_name == authorLastNew)).first()

                book = Books(titleNew,editionNew,yearNew,isbnNew,typeNew,pub_id.publisher_id)
                db.session.add(book)
                db.session.commit()
                contain = ContainsAsscociation(current_user.id,book.book_id,1,'YES')
                db.session.add(contain)
                db.session.commit()
                written = WrittenByAssociation(auth_id.author_id,book.book_id)
                db.session.add(written)
                db.session.commit()

                flash('Book successfully added', 'success')
                return redirect(url_for('profile',user_id = current_user.id,page_num=1))

            else:

                bookquantity = ContainsAsscociation.query.filter((ContainsAsscociation.shelf_id == current_user.id) & (ContainsAsscociation.book_id == books.book_id)).first()

                if bookquantity is None:
                    contain = ContainsAsscociation(current_user.id,books.book_id,1,'YES')
                    db.session.add(contain)
                    db.session.commit()

                else:
                    curQuant = bookquantity.quantity
                    bookquantity.quantity = int(curQuant+1)
                    db.session.commit()



                return redirect(url_for('profile',user_id = current_user.id,page_num=1))


        elif not form.validate():
            flash("Please don't leave any blank", 'error')
            return render_template("add.html", form=form)
        else:
            return render_template("add.html", form=form)


    else:
        return render_template("add.html", form=form)


@app.route('/delete', methods = ['POST', 'GET'])
@login_required
def deletefunc():
    deleteStore = request.form['Store']
    if request.method == 'POST':
        avail = ContainsAsscociation.query.filter(ContainsAsscociation.book_id == deleteStore).first()
        availDelete = int(avail.quantity)
        avail.quantity = availDelete-1
        db.session.commit()
        if avail.quantity == 0:
            avail.availability = 'No'
            db.session.commit()


        return redirect(url_for('profile',user_id = current_user.id,page_num=1))

    else:
        return redirect(url_for('profile',user_id = current_user.id,page_num=1))

@app.route('/updateBook', methods = ['POST', 'GET'])
@login_required
def updateGet():
    updateStore = request.form['Store']
    updatePub = request.form['Pub']

    if request.method == 'POST':
        session['bookidNew'] = updateStore
        session['PubNew'] = updatePub
        return redirect(url_for('update'))

    else:
        return redirect(url_for('profile', user_id = current_user.id , page_num=1))


@app.route('/updateForm', methods = ['POST', 'GET'])
@login_required
def update():

    form = Forms(request.form)
    bookidNew = session['bookidNew']
    bookidpub = session['PubNew']
    if request.method == 'POST':
        titleNew = form.titleNew.data
        yearNew = form.yearNew.data
        typeNew = form.typeNew.data
        editionNew = form.editionNew.data
        isbnNew = form.isbnNew.data
        publisherNew = form.publisher_id.data
        authorFirstNew = form.authorFirstNew.data
        authorLastNew = form.authorLastNew.data

        if form.validate():
            updateNew = Books.query.filter_by(book_id = bookidNew).first()
            updateAuthor = Author.query.filter_by(author_id = bookidNew).first()
            updatePublishers = Publisher.query.filter_by(publisher_id = bookidpub).first()

            if updatePublishers is None:
                addpub = Publisher(publisherNew)
                db.session.add(addpub)
                db.session.commit()

            updatePublishers = Publisher.query.filter_by(publisher_id = bookidpub).first()

            updateNew.title = titleNew
            updateNew.year_published = yearNew
            updateNew.types = typeNew
            updateAuthor.author_first_name = authorFirstNew
            updateAuthor.author_last_name = authorLastNew
            updatePublishers.publisher_name = publisherNew
            updateNew.edition = editionNew
            updateNew.isbn = isbnNew
            db.session.commit()

            return redirect(url_for('profile', user_id = current_user.id, page_num=1))

        elif not form.validate():
            flash('Please fill up each of the following', 'error')
            return render_template("update.html", form = form)

        else:
            return render_template("update.html", form = form)


    else:
        return render_template("update.html", form=form)

@app.route('/searchGet/<int:user_id>/<int:page_num>', methods = ['POST', 'GET'])
@login_required
def searchGet(user_id,page_num):
    search = request.form['search']
    search1 = "%"+search+"%"
    pags = ContainsAsscociation.query.join(Books).filter((Books.title.like(search1)) | (Books.year_published.like(search1)) | (Books.types.like(search1)) | (Books.edition.like(search1)) | (Books.isbn.like(search1))).paginate(page_num,6)
    form = EditProfile()
    foruserId = User.query.filter_by(id=user_id).first()
    if user_id == current_user.id:
        form = EditProfile()
        foruserId = User.query.filter_by(id=user_id).first()
        if request.method == 'POST':

            return redirect(url_for('searchGetImp', user_id = current_user.id , page_num=1, string1=search))

    elif user_id != current_user.id:
        form = User.query.filter_by(id=user_id).first()
        return redirect(url_for('searchGetImp', user_id = form.id , page_num=1, string1=search))

    return render_template('userSearch.html', pags = pags, data=current_user,form = form, userId=foruserId)


@app.route('/searchGet/<int:user_id>/<int:page_num>/<string:string1>', methods = ['POST', 'GET'])
@login_required
def searchGetImp(user_id,page_num,string1):
    session['stringNew'] = string1
    session['page'] = page_num
    session['forpage'] = 0
    if user_id == current_user.id:
        foruserId = User.query.filter_by(id=user_id).first()
        form = EditProfile()
        search = string1
        search1 = "%"+search+"%"
        pags = ContainsAsscociation.query.join(Books).filter((ContainsAsscociation.shelf_id == current_user.id) & (Books.title.like(search1)) | (Books.year_published.like(search1)) | (Books.types.like(search1)) | (Books.edition.like(search1)) | (Books.isbn.like(search1))).paginate(page_num,6)

        x=[]
        y=[]
        for p in pags.items:
            s = WrittenByAssociation.query.filter_by(book_id=p.book_id).first()
            author = Author.query.filter_by(author_id=s.author_id).first()
            x.append(author.author_first_name)
            y.append(author.author_last_name)

        return render_template('userSearch.html', pags = pags, data=current_user,form = form, string=string1, x=x, y=y)

    elif user_id != current_user.id:
        search = string1
        search1 = "%"+search+"%"
        form = User.query.filter_by(id=user_id).first()
        pags = ContainsAsscociation.query.join(Books).filter((ContainsAsscociation.shelf_id == user_id) & (Books.title.like(search1)) | (Books.year_published.like(search1)) | (Books.types.like(search1)) | (Books.edition.like(search1)) | (Books.isbn.like(search1))).paginate(page_num,6)

        x=[]
        y=[]
        for p in pags.items:
            s = WrittenByAssociation.query.filter_by(book_id=p.book_id).first()
            author = Author.query.filter_by(author_id=s.author_id).first()
            x.append(author.author_first_name)
            y.append(author.author_last_name)

        return render_template('userSearchDiffUser.html', pags = pags, data=current_user,form = form,string=string1, x=x, y=y)



# ang notif na himo ug id sa book
@app.route('/borrow', methods = ['POST', 'GET'])
@login_required
def borrow():
    page = session['page']
    otheruserId = request.form['userId']
    bookid = request.form['Store']

    pags = ContainsAsscociation.query.filter(ContainsAsscociation.shelf_id == otheruserId).first()
    bookBorrow = BorrowsAssociation.query.filter((BorrowsAssociation.user_id == current_user.id) & (BorrowsAssociation.shelf_id == otheruserId) & (BorrowsAssociation.bookid == bookid)).first()
    quant =int(pags.quantity)
    if bookBorrow is None:
        borrowBook = BorrowsAssociation(current_user.id,otheruserId,1,bookid)
        db.session.add(borrowBook)
        db.session.commit()
        flash("Book successfully borrowed", 'success')

        if session['forpage'] == 1:
            return redirect(url_for('profile',user_id = otheruserId,page_num=page))
        else:
            string = session['stringNew']
            return redirect(url_for('searchGetImp',user_id = otheruserId,page_num=page,string1 = string))

    elif bookBorrow is not None:
        flash("Book already borrowed", 'error')
        if session['forpage'] == 1:
            return redirect(url_for('profile',user_id = otheruserId,page_num=page))
        else:
            string = session['stringNew']
            return redirect(url_for('searchGetImp',user_id = otheruserId,page_num=page,string1 = string))

    elif (quant == 0):
        flash('Book not available', 'error')

        if session['forpage'] == 1:
            return redirect(url_for('profile',user_id = otheruserId,page_num=page))
        else:
            string = session['stringNew']
            return redirect(url_for('searchGetImp',user_id = otheruserId,page_num=page,string1 = string))

@app.route('/rateBook', methods = ['POST', 'GET'])
@login_required
def rateBook():
    page = session['page']
    bookid = request.form['Store']
    rateNew = request.form['rate']
    otheruserId = request.form['userId']

    rateOld = BookRateAssociation.query.filter((BookRateAssociation.user_id == current_user.id) & (BookRateAssociation.book_id == bookid)).first()

    if rateOld is not None:
        rateOld.rating = rateNew
        db.session.commit()

        totOld = BookRateTotal.query.filter(BookRateTotal.bookRated == bookid).first()
        if totOld is not None:
            rateTot = BookRateAssociation.query.filter(BookRateAssociation.book_id == bookid).paginate(page,6)

            x=0
            count=0
            for p in rateTot.items:
                r = int(p.rating)
                x= float(x+r)
                count = float(count+1)

            totRate = float(x/count)
            totOld.totalRate = totRate
            db.session.commit()
        else:
            rateTot = BookRateAssociation.query.filter(BookRateAssociation.book_id == bookid).paginate(page,6)

            x=0
            count=0
            for p in rateTot.items:
                r = int(p.rating)
                x= float(x+r)
                count = float(count+1)

            totRate = float(x/count)

            newRateTot = BookRateTotal(current_user.id,bookid,totRate)
            db.session.add(newRateTot)
            db.session.commit()


        if session['forpage'] == 1:
            return redirect(url_for('profile',user_id = otheruserId,page_num=page))
        else:
            string = session['stringNew']
            return redirect(url_for('searchGetImp',user_id = otheruserId,page_num=page,string1 = string))



    else:
        newRater =  BookRateAssociation(current_user.id,bookid,rateNew)
        db.session.add(newRater)
        db.session.commit()

        totOld = BookRateTotal.query.filter(BookRateTotal.bookRated == bookid).first()
        if totOld is not None:
            rateTot = BookRateAssociation.query.filter(BookRateAssociation.book_id == bookid).paginate(page,6)

            x=0
            count=0
            for p in rateTot.items:
                r = int(p.rating)
                x= float(x+r)
                count = float(count+1)

            totRate = float(x/count)
            totOld.totalRate = totRate
            db.session.commit()
        else:
            rateTot = BookRateAssociation.query.filter(BookRateAssociation.book_id == bookid).paginate(page,6)

            x=0
            count=0
            for p in rateTot.items:
                r = int(p.rating)
                x= float(x+r)
                count = float(count+1)

            totRate = float(x/count)

            newRateTot = BookRateTotal(current_user.id,bookid,totRate)
            db.session.add(newRateTot)
            db.session.commit()

        if session['forpage'] == 1:
            return redirect(url_for('profile',user_id = otheruserId,page_num=page))
        else:
            string = session['stringNew']
            return redirect(url_for('searchGetImp',user_id = otheruserId,page_num=page,string1 = string))


@app.route('/rateUser', methods = ['POST', 'GET'])
@login_required
def rateUser():
    page = session['page']
    rateNew = request.form['rateUser']
    otheruserId = request.form['userId']

    rateOld = UserRateAssociation.query.filter((UserRateAssociation.user_idRatee == otheruserId) & (UserRateAssociation.user_idRater == current_user.id)).first()

    if rateOld is not None:
        rateOld.rating = rateNew
        db.session.commit()

        totOld = UserRateTotal.query.filter(UserRateTotal.userRatee == otheruserId).first()
        if totOld is not None:
            rateTot = UserRateAssociation.query.filter(UserRateAssociation.user_idRatee == otheruserId).paginate(page,6)

            x=0
            count=0
            for p in rateTot.items:
                r = int(p.rating)
                x= float(x+r)
                count = float(count+1)

            totRate = float(x/count)
            totOld.totalRate = totRate
            db.session.commit()
        else:
            rateTot = UserRateAssociation.query.filter(UserRateAssociation.user_idRatee == otheruserId).paginate(page,6)

            x=0
            count=0
            for p in rateTot.items:
                r = int(p.rating)
                x= float(x+r)
                count = float(count+1)

            totRate = float(x/count)

            newRateTot = UserRateTotal(otheruserId,current_user.id,totRate)
            db.session.add(newRateTot)
            db.session.commit()


        if session['forpage'] == 1:
            return redirect(url_for('profile',user_id = otheruserId,page_num=page))
        else:
            string = session['stringNew']
            return redirect(url_for('searchGetImp',user_id = otheruserId,page_num=page,string1 = string))



    else:

        newRater = UserRateAssociation(current_user.id,otheruserId,rateNew)
        db.session.add(newRater)
        db.session.commit()

        totOld = UserRateTotal.query.filter(UserRateTotal.userRatee == otheruserId).first()
        if totOld is not None:
            rateTot = UserRateAssociation.query.filter(UserRateAssociation.user_idRatee == otheruserId).paginate(page,6)

            x=0
            count=0
            for p in rateTot.items:
                r = int(p.rating)
                x= float(x+r)
                count = float(count+1)

            totRate = float(x/count)
            totOld.totalRate = totRate
            db.session.commit()
        else:
            rateTot = UserRateAssociation.query.filter(UserRateAssociation.user_idRatee == otheruserId).paginate(page,6)

            x=0
            count=0
            for p in rateTot.items:
                r = int(p.rating)
                x= float(x+r)
                count = float(count+1)

            totRate = float(x/count)

            newRateTot = UserRateTotal(otheruserId,current_user.id,totRate)
            db.session.add(newRateTot)
            db.session.commit()

        if session['forpage'] == 1:
            return redirect(url_for('profile',user_id = otheruserId,page_num=page))
        else:
            string = session['stringNew']
            return redirect(url_for('searchGetImp',user_id = otheruserId,page_num=page,string1 = string))


@app.route('/commentPage', methods = ['POST', 'GET'])
@login_required
def commentPage():
    formComment = CommentForms(request.form)
    page = session['page']
    userIdNew = request.form['Store']

    if request.method == 'POST':
        com = formComment.commentNew.data

        if formComment.validate():
            commenter = UserComment(current_user.id,userIdNew,com)
            db.session.add(commenter)
            db.session.commit()

            if session['forpage'] == 1:
                return redirect(url_for('profile',user_id = userIdNew,page_num=page))
            else:
                string = session['stringNew']
                return redirect(url_for('searchGetImp',user_id = userIdNew,page_num=page,string1 = string))

        else:

            if session['forpage'] == 1:
                return redirect(url_for('profile',user_id = userIdNew,page_num=page))
            else:
                string = session['stringNew']
                return redirect(url_for('searchGetImp',user_id = userIdNew,page_num=page,string1 = string))

    else:
        return redirect(url_for('profile',user_id = userIdNew,page_num=page))



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
