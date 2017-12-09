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
        '''
        elif request.method == 'POST':
            ratingNew = int(request.form['rate'])
            bookidNew = request.form['Store']
            if ratingNew > 0:
                userRate = Shelf.query.filter_by(bookid=bookidNew).first()
                rate = userRate.rating
                raters = userRate.raters

                dividend = ratingNew+rate
                ratersTot = raters+1

                total = float(dividend/ratersTot)

                userRate.rating = total
                userRate.raters = ratersTot
                db.session.commit()

                pags = Shelf.query.filter_by(owner_id=current_user.id).paginate(page_num,10)
            
            else:
                pass

            form = EditProfile()
            return render_template('profile.html', pags = pags, data=current_user,form = form)
            '''

    elif user_id != current_user:
        pags = Shelf.query.filter_by(owner_id=user_id).paginate(page_num,10)
        form = Users.query.filter_by(id=user_id).first()
        return render_template('diffuser.html', pags = pags, data=current_user,form = form)

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


            if books is None:
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
                contain = ContainsAsscociation(current_user.id,book.book_id,1)
                db.session.add(contain)
                db.session.commit()
                written = WrittenByAssociation(auth_id.author_id,book.book_id)
                db.session.add(written)
                db.session.commit()

                flash('Book successfully added', 'success')
                return redirect(url_for('profile',user_id = current_user.id,page_num=1))
            else:

                bookquantity = ContainsAsscociation.query.filter(ContainsAsscociation.shelf_id == current_user.id and ContainsAsscociation.book_id == books.book_id).first()
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

        return redirect(url_for('profile',user_id = current_user.id,page_num=1))

    else:
        return redirect(url_for('profile',user_id = current_user.id,page_num=1))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
