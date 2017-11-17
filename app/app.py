from flask import Flask, render_template, flash, url_for, redirect
from forms import *
from models import *
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.secret_key = '31498657699432922335'
app.debug = True
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


@app.route('/')
def index():
    if current_user.is_authenticated is True:
        return redirect(url_for('home'))
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if current_user.is_authenticated is True:
        return redirect(url_for('home'))
    elif form.validate_on_submit():
        hashed = generate_password_hash(form.password.data, method='sha256')
        new_user = Users(form.username.data, hashed, form.first_name.data,
                         form.last_name.data, form.middle_initial.data, form.contact.data, form.sex.data,
                         form.year.data+'-'+form.month.data+'-'+form.day.data)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        return redirect(url_for('home'))
    return render_template('registration.html', form=form)


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


@app.route('/home')
@login_required
def home():
    return render_template('dashboard.html', name=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = EditProfile()
    if form.validate_on_submit():
        update = Users.query.filter_by(id=current_user.id).first()
        update.first_name = form.first_name.data
        update.last_name = form.last_name.data
        update.middle_initial = form.middle_initial.data
        update.contact_number = form.contact.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('profile.html', data=current_user, form=form)
if __name__ == '__main__':
    app.run()
