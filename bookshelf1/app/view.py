from app import app, RegistrationForm, Users, db, LoginForm, Search, Books
from flask import render_template, redirect, url_for, flash
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from werkzeug.security import check_password_hash

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


@app.route('/', methods=['GET', 'POST'])
def index():
    searchform = Search()
    if current_user.is_authenticated is True:
        return redirect(url_for('home'))
    else:
        if searchform.validate_on_submit():
            pass
        else:
            top = Books.query.order_by(Books.rating.desc()).limit(6).all()
            return render_template('index.html', searchform=searchform, top=top)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated is True:
        return redirect(url_for('home'))
    elif form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
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
        new_user = Users(form.username.data, form.password.data, form.first_name.data,
                         form.last_name.data, form.contact.data, form.sex.data,
                         form.year.data+'-'+form.month.data+'-'+form.day.data)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route('/home')
@login_required
def home():
    return 'home'


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
