from app import app, User, Search, LoginForm, RegistrationForm, db, Author, Books, WrittenByAssociation
from flask import render_template, redirect, url_for, flash
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from werkzeug.security import check_password_hash

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/', methods=['GET', 'POST'])
def index():
    wordtosearch = Search()
    if current_user.is_authenticated is True:
        return redirect(url_for('home'))
    else:
        if wordtosearch.validate_on_submit():
            pass
        else:

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
        new_user = User(form.username.data, form.password.data, form.first_name.data,
                        form.last_name.data, form.contact.data, form.year.data+'-'+form.month.data+'-'+form.day.data,
                        form.sex.data)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route('/home', defaults={'page_num': 1})
@app.route('/home/<int:page_num>', methods=['GET', 'POST'])
@login_required
def home(page_num):
    books = Books.query.join(Books.rateBooks).join(Books.booksAuthor).paginate(per_page=9, page=page_num, error_out=True)
    return render_template('homepage.html', books=books, current_user=current_user)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html', current_user=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
