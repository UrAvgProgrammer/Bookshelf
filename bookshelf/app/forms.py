from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, RadioField, SelectField, ValidationError
from wtforms.validators import Length, InputRequired, EqualTo, DataRequired
from models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=3, max=25)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=80)])
    confirm = PasswordField('Repeat password', validators=[DataRequired(),
                                                           EqualTo('password', message='Passwords must match.')])
    first_name = StringField('First name', validators=[InputRequired(), Length(min=3, max=25)])
    last_name = StringField('Last name', validators=[InputRequired(), Length(min=2, max=25)])
    contact = StringField('Contact', validators=[InputRequired(), Length(11)])
    sex = RadioField('Sex', validators=[InputRequired()], choices=[('M', 'Male'), ('F', 'Female')], default='M')
    month = SelectField('', choices=[('01', 'January'), ('02', 'February'), ('03', 'March'),
                                               ('04', 'April'), ('05', 'May'), ('06', 'June'),
                                               ('07', 'July'), ('08', 'August'), ('09', 'September'),
                                               ('10', 'October'), ('11', 'November'), ('12', 'December')])
    day = SelectField('', choices=[('01', '1'), ('02', '2'), ('03', '3'), ('04', '4'), ('05', '5'),
                                   ('06', '6'), ('07', '7'), ('08', '8'), ('09', '9'), ('10', '10'),
                                   ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'),
                                   ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'),
                                   ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'),
                                   ('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'),
                                   ('29', '29'), ('30', '30'), ('31', '31')])
    year = SelectField('', choices=[('2017', '2017'), ('2016', '2016'), ('2015', '2015'), ('2014', '2014'),
                                    ('2013', '2013'), ('2012', '2012'), ('2011', '2011'), ('2010', '2010'),
                                    ('2009', '2009'), ('2008', '2008'), ('2007', '2007'), ('2006', '2006'),
                                    ('2005', '2005'), ('2004', '2004'), ('2003', '2003'), ('2002', '2002'),
                                    ('2001', '2001'), ('2000', '2000'), ('1999', '1999'), ('1998', '1998'),
                                    ('1997', '1997'), ('1996', '1996'), ('1995', '1995'), ('1994', '1994'),
                                    ('1993', '1993'), ('1992', '1992'), ('1991', '1991'), ('1990', '1990'),
                                    ('1989', '1989'), ('1988', '1988'), ('1987', '1987'), ('1986', '1986'),
                                    ('1985', '1985'), ('1984', '1984'), ('1983', '1983'), ('1982', '1982'),
                                    ('1981', '1981'), ('1980', '1980'), ('1979', '1979'), ('1978', '1978'),
                                    ('1977', '1977'), ('1976', '1976'), ('1975', '1975'), ('1974', '1974'),
                                    ('1973', '1973'), ('1972', '1972'), ('1971', '1971'), ('1970', '1970')])

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class LoginForm(FlaskForm):
    username = StringField('Username', [InputRequired(message='Username is invalid'), Length(min=3, max=25)])
    password = PasswordField('Password', [InputRequired(message='Password is invalid'), Length(min=6, max=80)])

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first() is None:
            raise ValidationError('Username is not registered')


class EditProfile(FlaskForm):
    first_name = StringField('First name', validators=[InputRequired(), Length(min=3, max=25)])
    last_name = StringField('Last name', validators=[InputRequired(), Length(min=2, max=25)])
    contact = StringField('Contact', validators=[InputRequired(), Length(11)])
    submit = SubmitField('Update')


class Search(FlaskForm):
    search = StringField(validators=[InputRequired()])


class EditProfile(FlaskForm):
    first_name = StringField('First name', validators=[InputRequired(), Length(min=3, max=25)])
    last_name = StringField('Last name', validators=[InputRequired(), Length(min=2, max=25)])
    middle_initial = StringField('Middle initial', validators=[InputRequired(),
                                                               Length(min=1, message='1 character only', max=1)])
    contact = StringField('Contact', validators=[InputRequired(), Length(11)])
    submit = SubmitField('Update')


class Forms(FlaskForm):
    titleNew = StringField('Title', validators=[Length(min=1, max=40)])
    yearNew = StringField('Year Published', validators=[Length(min=1, max=10)])
    typeNew = StringField('Book Type', validators=[Length(min=1, max=20)])
    authorNew = StringField('Author', validators=[Length(min=1, max=40)])
    editionNew = StringField('Edition', validators=[Length(min=1, max=20)])
    isbnNew = StringField('ISBN', validators=[Length(min=1, max=30)])
    submit = SubmitField("Submit")


class BookForms(FlaskForm):
    bookidNew = StringField('Book ID', validators=[Length(min=1, max=60)])
    submit = SubmitField("Submit")
